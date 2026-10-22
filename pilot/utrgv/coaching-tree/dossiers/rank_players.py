#!/usr/bin/env python3
"""Rank coaching-tree players: NFL first, then production (honors), then PFF grade, highest to lowest.
Adds nfl_level, honor_level, pff_best (grade, season, team, source) to each player row in coaching_tree.json,
re-sorts TOP and LOW lists, and rewrites the flattened CSV.
"""
import csv, json, re, sys, unicodedata
from pathlib import Path
import pandas as pd

TREE = Path(sys.argv[1])            # coaching_tree.json (in/out)
PFF_DIR = Path(sys.argv[2])         # edge3-pff-integration/data/pff/ncaa
OUT_CSV = Path(sys.argv[3])

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)", "", s)            # drop parentheticals
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b\.?", "", s, flags=re.I)
    s = re.sub(r"[^a-z ]", "", s.lower())
    return re.sub(r"\s+", " ", s).strip()

# ---- PFF: one row per player-season with best available grade
frames = []
for fn, gcol, side in [("pff_passing_2014_2025.csv", "grades_offense", "passing"),
                       ("pff_receiving_2014_2025.csv", "grades_offense", "receiving"),
                       ("pff_rushing_2014_2025.csv", "grades_offense", "rushing"),
                       ("pff_blocking_2014_2025.csv", "grades_offense", "blocking"),
                       ("pff_defense_2014_2025.csv", "grades_defense", "defense")]:
    df = pd.read_csv(PFF_DIR / fn, usecols=lambda c: c in {"player", "position", "team_name", "season", gcol, "player_game_count"})
    df = df.rename(columns={gcol: "grade"})
    df["source"] = side
    frames.append(df)
pff = pd.concat(frames, ignore_index=True)
pff["key"] = pff["player"].map(norm)
pff = pff.dropna(subset=["grade"])
pff["season"] = pff["season"].astype(int)

def years_of(text):
    ys = [int(y) for y in re.findall(r"(?<!\d)(20\d\d|19\d\d)(?!\d)", str(text))]
    # handle "2018-20" / "2018–20"
    for a, b in re.findall(r"(20\d\d)\s*[–-]\s*(\d\d)(?!\d)", str(text)):
        ys.append(int(a[:2] + b))
    if not ys:
        return None
    return (min(ys), max(ys))

STOP_TEAM = [("houston", "HOUSTON"), ("louisiana tech", "LA TECH"), ("texas state", "TEXAS ST"), ("arizona", "ARIZONA"),
             ("utep", "UTEP"), ("texas tech", "TEXAS TECH"), ("south alabama", "S ALABAMA"), ("oklahoma state", "OKLA STATE"),
             ("utsa", "UTSA"), ("marshall", "MARSHALL")]
def stop_team(stop):
    t = stop.lower()
    for k, v in STOP_TEAM:
        if k in t:
            return v
    return None
def pos_source(pos):
    p = str(pos).upper()
    if p.startswith("QB"): return "passing"
    if p.startswith(("RB", "HB", "FB")): return "rushing"
    if p.startswith(("WR", "TE", "KR")): return "receiving"
    if p.startswith(("OL", "OT", "OG", "C", "T", "G", "FB / C")): return "blocking"
    if p.startswith(("LB", "ILB", "OLB", "DE", "DL", "DT", "NT", "EDGE", "S", "CB", "DB", "FS", "SS")): return "defense"
    return None
def pff_best(name, yrs, team=None, pos=None):
    k = norm(name)
    if not k or team is None:
        return None
    rows = pff[(pff.key == k) & (pff.team_name == team)]
    if yrs:
        rows = rows[(rows.season >= yrs[0]) & (rows.season <= yrs[1])]
    src = pos_source(pos)
    if src and (rows.source == src).any():
        rows = rows[rows.source == src]
    if rows.empty:
        return None
    r = rows.sort_values("grade", ascending=False).iloc[0]
    return {"grade": float(r.grade), "season": int(r.season), "team": str(r.team_name), "pos": str(r.position), "source": str(r.source)}

NFL_RULES = [
    (3, r"pro bowl|all-pro|first.round|no\. ?\d+ overall|\b(1st|2nd|3rd|4th|5th|6th|7th)[- ]r(oun)?d\b|round, no\.|nfl draft \(|drafted|super bowl|nfl (games|roster)"),
    (2, r"udfa|undrafted|practice squad|\bps\b|minicamp|nfl liaison|arena|cfl|afl|ifl|ufl"),
]
# refine: a listed NFL coach-player row (Bills 2015) is level 3 by definition
HONOR_RULES = [
    (6, r"all-american|all-america|aa\b|walter payton|harlon hill|player of the year|\bpoy\b|opoy|dpoy"),
    (5, r"1st[- ]team all|first[- ]team all|first team all"),
    (4, r"2nd[- ]team all|second[- ]team all|newcomer of the year|freshman of the year|rookie of the year|all-freshman"),
    (3, r"3rd[- ]team|hm all|honorable mention|4th team|all-region|academic all"),
    (2, r"school record|program record|led (the )?team|team-high|team-best|led (league|conference|nation)|single[- ]season|career passing leader|all-time|(?<!\\d)\\d,\\d{3} (pass )?yds"),
    (1, r"\d"),
]

def level(text, rules):
    t = str(text).lower()
    for lv, pat in rules:
        if re.search(pat, t):
            return lv
    return 0

tree = json.loads(TREE.read_text())
flat = []
for c in tree["coaches"]:
    for s in c["stops"]:
        stop_yrs = years_of(s["stop"])
        for tier in ("top", "low"):
            for p in s[tier]:
                yrs = years_of(p["years"]) or stop_yrs
                txt = p["outcome"] + " " + p["player"]
                p["nfl_level"] = level(txt, NFL_RULES)
                if "bills" in s["stop"].lower():
                    p["nfl_level"] = 3
                p["honor_level"] = level(p["outcome"], HONOR_RULES)
                pb = pff_best(p["player"], yrs, stop_team(s["stop"]), p["pos"])
                p["pff_best"] = pb
                p["rank_key"] = [p["nfl_level"], p["honor_level"], pb["grade"] if pb else -1]
            s[tier].sort(key=lambda r: tuple(r["rank_key"]), reverse=True)
            for i, p in enumerate(s[tier], 1):
                p["rank"] = i
                flat.append({"coach": c["coach"], "utrgv_title": c["utrgv_title"], "stop": s["stop"], "tier": tier.upper(),
                             "rank": i, "player": p["player"], "pos": p["pos"], "years": p["years"],
                             "nfl_level": p["nfl_level"], "honor_level": p["honor_level"],
                             "pff_best_grade": pb["grade"] if (pb := p["pff_best"]) else "",
                             "pff_season": pb["season"] if pb else "", "pff_team": pb["team"] if pb else "",
                             "pff_source": pb["source"] if pb else "",
                             "outcome": p["outcome"], "sources": " ; ".join(p["sources"])})
tree["meta"]["ranking_rule"] = ("Within each stop, TOP and LOW lists are sorted highest to lowest by: (1) NFL outcome "
    "(3 = drafted, NFL roster or NFL honors; 2 = UDFA, camp, practice squad or other pro league; 0 = none), "
    "(2) production (6 = All-American or conference/national player of the year; 5 = first-team all-conference; "
    "4 = second-team, freshman/newcomer/rookie of the year; 3 = third-team, honorable mention, all-region or academic; "
    "2 = records or team-leading stats; 1 = stats only), (3) best PFF season grade during the coach's years at that stop "
    "(FBS 2014 to 2025 only; blank means no PFF row, which is expected for FCS, D2, JUCO, HS and pre-2014 stops).")
tree["meta"]["pff_source"] = "edge3-model/edge3-pff-integration/data/pff/ncaa/pff_{passing,receiving,rushing,blocking,defense}_2014_2025.csv"
TREE.write_text(json.dumps(tree, indent=2, ensure_ascii=False))
with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(flat[0].keys())); w.writeheader(); w.writerows(flat)
n_pff = sum(1 for r in flat if r["pff_best_grade"] != "")
print(f"rows={len(flat)} with_pff={n_pff}")
for r in flat:
    if r["pff_best_grade"] != "":
        print(f"  {r['coach'][:14]:<14} {r['player'][:28]:<28} {r['years']:<10} PFF {r['pff_best_grade']:>5} {r['pff_season']} {r['pff_team']} ({r['pff_source']}) nfl={r['nfl_level']} honor={r['honor_level']}")
