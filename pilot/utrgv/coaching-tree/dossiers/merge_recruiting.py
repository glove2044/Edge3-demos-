#!/usr/bin/env python3
"""Merge agent recruiting-profile JSON (out/recruit_web_*.json) into coaching_tree.json rows,
rewrite the flattened players CSV with recruiting columns, and print a coverage summary."""
import csv, json, re, sys
from pathlib import Path

TREE = Path(sys.argv[1]); WEB_GLOB = sys.argv[2]; OUT_CSV = Path(sys.argv[3])

def nk(s): return re.sub(r"[^a-z ]", "", re.sub(r"\(.*?\)", "", str(s)).lower()).strip()

web = {}
for f in sorted(Path(".").glob(WEB_GLOB)):
    try:
        data = json.loads(f.read_text())
    except Exception as e:
        print("bad json", f, e); continue
    rows = data if isinstance(data, list) else data.get("players", data.get("results", []))
    for r in rows:
        if isinstance(r, dict) and r.get("player"):
            web.setdefault(nk(r["player"]), r)
print("web profiles:", len(web))

tree = json.loads(TREE.read_text())
flat = []; filled = 0; total = 0
for c in tree["coaches"]:
    for s in c["stops"]:
        for tier in ("top", "low"):
            for p in s[tier]:
                total += 1
                pr = p.setdefault("recruit_profile", {})
                # multi-name rows: try each name
                names = [n.strip() for n in re.split(r",|/", re.sub(r"\(.*?\)", "", p["player"])) if n.strip()]
                w = None
                for n in names:
                    if nk(n) in web:
                        w = web[nk(n)]; break
                if w:
                    for k in ("class_year", "stars_247", "composite_247", "stars_rivals", "rivals_rating", "national_rank_247",
                              "position_rank_247", "state_rank_247", "hs_name", "hs_city", "hs_state", "origin",
                              "height_signing", "weight_signing", "hs_stats", "hs_honors", "combine", "confidence", "notes"):
                        v = w.get(k)
                        if v not in (None, "", [], {}):
                            if k in pr and pr[k] not in (None, "") and k in ("class_year", "stars_247", "composite_247", "hs_name", "hs_city", "hs_state"):
                                if str(pr[k]) != str(v):
                                    pr.setdefault("disagreements", []).append(f"{k}: local={pr[k]} web={v}")
                                if pr.get("match_status", "").startswith("unverified"):
                                    pr[k] = v
                            else:
                                pr[k] = v
                    pr["sources_web"] = w.get("sources", [])
                    pr["match_status"] = pr.get("match_status", "") + "; web pass done"
                if any(pr.get(k) not in (None, "") for k in ("stars_247", "composite_247", "hs_name", "height_signing")):
                    filled += 1
                cb = pr.get("combine") if isinstance(pr.get("combine"), dict) else {}
                flat.append({"coach": c["coach"], "utrgv_title": c["utrgv_title"], "stop": s["stop"], "tier": tier.upper(), "rank": p.get("rank"),
                             "player": p["player"], "pos": p["pos"], "years": p["years"],
                             "nfl_level": p.get("nfl_level"), "honor_level": p.get("honor_level"),
                             "pff_best_grade": (p.get("pff_best") or {}).get("grade", ""), "pff_season": (p.get("pff_best") or {}).get("season", ""),
                             "recruit_class": pr.get("class_year", ""), "stars_247": pr.get("stars_247", ""), "composite_247": pr.get("composite_247", ""),
                             "stars_rivals": pr.get("stars_rivals", ""), "national_rank_247": pr.get("national_rank_247", ""),
                             "hs_name": pr.get("hs_name", ""), "hs_city": pr.get("hs_city", ""), "hs_state": pr.get("hs_state", ""),
                             "origin": pr.get("origin", ""), "height_signing": pr.get("height_signing", ""), "weight_signing": pr.get("weight_signing", ""),
                             "hs_stats": pr.get("hs_stats", ""), "hs_honors": pr.get("hs_honors", ""),
                             "forty": cb.get("forty", ""), "shuttle": cb.get("shuttle", ""), "vertical": cb.get("vertical", ""), "broad": cb.get("broad", ""),
                             "combine_source": cb.get("source", ""), "hs_competitive_index": pr.get("hs_competitive_index", ""),
                             "recruit_match_status": pr.get("match_status", ""), "recruit_confidence": pr.get("confidence", ""),
                             "outcome": p["outcome"], "sources": " ; ".join(p["sources"]), "recruit_sources": " ; ".join(pr.get("sources_web", []) + pr.get("source_local", []))})
TREE.write_text(json.dumps(tree, indent=2, ensure_ascii=False))
with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(flat[0].keys())); w.writeheader(); w.writerows(flat)
n_comb = sum(1 for r in flat if r["forty"] not in ("", None))
n_hw = sum(1 for r in flat if r["height_signing"] not in ("", None))
n_stars = sum(1 for r in flat if r["stars_247"] not in ("", None))
print(f"rows={total} with_recruit_profile={filled} with_stars={n_stars} with_height_weight={n_hw} with_forty={n_comb}")
