#!/usr/bin/env python3
"""Join every coaching-tree player to local recruiting / HS profile data in edge3-model:
   - 247 composite + HS (fb_player_ci_proxy.csv: 247Stars, 247CompositeScore, HighSchool, city, state, HS_CompetitiveIndex)
   - CFBD recruits 2018-2026 (stars, rating, national ranking, HS city/state, committedTo)
Writes recruit_profile onto each player row in coaching_tree.json and a gap list for the web pass.
"""
import json, re, sys, unicodedata
from pathlib import Path
import pandas as pd

TREE = Path(sys.argv[1]); MODEL = Path(sys.argv[2]); GAPS = Path(sys.argv[3])

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b\.?", "", s, flags=re.I)
    s = re.sub(r"[^a-z ]", "", s.lower())
    return re.sub(r"\s+", " ", s).strip()

def years_of(text):
    ys = [int(y) for y in re.findall(r"(?<!\d)(20\d\d|19\d\d)(?!\d)", str(text))]
    for a, b in re.findall(r"(20\d\d)\s*[–-]\s*(\d\d)(?!\d)", str(text)):
        ys.append(int(a[:2] + b))
    return (min(ys), max(ys)) if ys else None

ci = pd.read_csv(MODEL / "models/transfer-risk/intelligence/competitive-index/fb_player_ci_proxy.csv")
ci["key"] = ci.PlayerName.map(norm)
rec = pd.read_csv(MODEL / "data/cfbd/recruits_2018_2026.csv")
rec["key"] = rec.name.map(norm)

def pick(df, ycol, first_year):
    """closest class year at or before the player's first documented college season (allow +1 for redshirt confusion)."""
    if df.empty:
        return None, 0
    if first_year:
        d = df[(df[ycol] <= first_year + 1) & (df[ycol] >= first_year - 5)].copy()
        if d.empty:
            return None, len(df)
        d["dist"] = (first_year - d[ycol]).abs()
        d = d.sort_values("dist")
        return d.iloc[0], len(d)
    return df.iloc[0], len(df)

tree = json.loads(TREE.read_text())
gaps = []; hit = 0; total = 0
for c in tree["coaches"]:
    for s in c["stops"]:
        stop_yrs = years_of(s["stop"])
        for tier in ("top", "low"):
            for p in s[tier]:
                total += 1
                yrs = years_of(p["years"]) or stop_yrs
                fy = yrs[0] if yrs else None
                k = norm(p["player"])
                prof = {"source_local": []}
                r, n = pick(ci[ci.key == k], "ClassYear", fy)
                if r is not None:
                    prof.update({"class_year": int(r.ClassYear), "stars_247": None if pd.isna(r["247Stars"]) else int(r["247Stars"]),
                                 "composite_247": None if pd.isna(r["247CompositeScore"]) else float(r["247CompositeScore"]),
                                 "hs_name": r.HighSchool, "hs_city": r.HighSchoolCity, "hs_state": r.HighSchoolState,
                                 "hs_competitive_index": None if pd.isna(r.HS_CompetitiveIndex) else float(r.HS_CompetitiveIndex),
                                 "hs_ci_tier": r.HS_CompetitiveIndex_Tier if isinstance(r.HS_CompetitiveIndex_Tier, str) else None})
                    prof["source_local"].append(f"247 composite via edge3-model fb_player_ci_proxy.csv (class {int(r.ClassYear)}{', ambiguous: %d candidates' % n if n > 1 else ''})")
                r2, n2 = pick(rec[rec.key == k], "year", fy)
                if r2 is not None:
                    prof.setdefault("class_year", int(r2.year))
                    prof.setdefault("stars_247", None if pd.isna(r2.stars) else int(r2.stars))
                    prof.setdefault("composite_247", None if pd.isna(r2.rating) else float(r2.rating))
                    prof["national_rank"] = None if pd.isna(r2.ranking) else int(r2.ranking)
                    prof.setdefault("hs_name", r2.school); prof.setdefault("hs_city", r2.city); prof.setdefault("hs_state", r2.stateProvince)
                    prof["committed_to"] = r2.committedTo; prof["recruit_classification"] = r2.classification
                    prof["source_local"].append(f"CFBD recruits (class {int(r2.year)}{', ambiguous: %d candidates' % n2 if n2 > 1 else ''})")
                if len(prof) > 1:
                    hit += 1
                else:
                    gaps.append({"coach": c["coach"], "stop": s["stop"], "tier": tier.upper(), "player": p["player"], "pos": p["pos"], "years": p["years"], "outcome": p["outcome"][:160]})
                p["recruit_profile"] = prof
TREE.write_text(json.dumps(tree, indent=2, ensure_ascii=False))
GAPS.write_text(json.dumps(gaps, indent=2, ensure_ascii=False))
print(f"rows={total} local_hits={hit} gaps={len(gaps)}")
for c in tree["coaches"]:
    for s in c["stops"]:
        for tier in ("top", "low"):
            for p in s[tier]:
                pr = p["recruit_profile"]
                if len(pr) > 1:
                    print(f"  {c['coach'][:12]:<12} {p['player'][:26]:<26} {p['years']:<10} class={pr.get('class_year')} {pr.get('stars_247')}* {pr.get('composite_247')} {pr.get('hs_name')} {pr.get('hs_city')},{pr.get('hs_state')} rank={pr.get('national_rank')} -> {pr.get('committed_to')}")
