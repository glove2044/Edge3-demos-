#!/usr/bin/env python3
"""Build the live-pilot package from coaching_tree.json:
  out/pilot/coaching_tree_coaches.csv, _stops.csv, _players.csv   (seed for the CoachStaff/CoachStop/CoachTreePlayer reference tables)
  out/pilot/player_facts_utrgv.csv                                 (rows for the platform's PlayerFact table, UTRGV players only)
  out/pilot/system_view_utrgv.json                                 (System view block in the New Mexico demo pattern)
"""
import csv, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path
import pandas as pd

TREE = Path(sys.argv[1]); MODEL = Path(sys.argv[2]); OUT = Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
tree = json.loads(TREE.read_text())
TEAM = "UT Rio Grande Valley"

def nk(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b\.?", "", s, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z ]", "", s.lower())).strip()
def slug(s): return re.sub(r"[^a-z0-9]+", "-", nk(s)).strip("-")

# ---- UTRGV roster join keys
ids = {}
r25 = pd.read_csv(MODEL / "data/fcs/utrgv_roster_2025_cfbd.csv")
for _, r in r25.iterrows():
    if pd.notna(r.cfbd_player_id): ids[nk(r.player_name)] = str(int(r.cfbd_player_id))
lov = pd.read_csv(MODEL / "data/fcs/utrgv_players_2026_lovable.csv", usecols=["player_name", "cfbd_player_id"])
for _, r in lov.iterrows():
    if pd.notna(r.cfbd_player_id): ids.setdefault(nk(r.player_name), str(int(r.cfbd_player_id)))

ROOM = {"Travis Bush": "HC", "Theron Aych": "QB", "Marco Regalado": "RB", "Gunnar Henderson": "WR", "Mike Barela": "TE",
        "Jeff Bowen": "OL", "Nate (Nathan) Langford": "DL", "James Lockhart IV": "EDGE", "Brian Gamble": "LB",
        "Adrian McDonald": "S", "Josh Jones": "CB"}

# ---- 1. coaches / stops / players seeds
coaches_rows, stops_rows, players_rows, facts = [], [], [], []
by_coach = {}
for c in tree["coaches"]:
    cid = slug(c["coach"]); by_coach[c["coach"]] = c
    conf = c.get("confidence", "")
    coaches_rows.append({"coach_id": cid, "coach_name": c["coach"], "utrgv_title": c["utrgv_title"], "room": ROOM.get(c["coach"], ""),
                         "mentors": " | ".join(c["mentors"]), "archetype_read": " | ".join(c["archetype"]),
                         "hc_archetype": " | ".join(c.get("hc_archetype", [])), "confidence": conf, "gaps": c["gaps"],
                         "source_dossier": c["source_file"]})
    for i, t in enumerate(c["timeline"], 1):
        stops_rows.append({"coach_id": cid, "stop_order": i, "years": t["years"], "school": t["school"], "role": t["role"],
                           "worked_under": t["worked_under"], "sources": " ; ".join(t["sources"])})
    for s in c["stops"]:
        for tier in ("top", "low"):
            for p in s[tier]:
                pr = p.get("recruit_profile") or {}; cb = pr.get("combine") if isinstance(pr.get("combine"), dict) else {}
                pb = p.get("pff_best") or {}
                is_utrgv = "UTRGV" in s["stop"]
                cfbd = ids.get(nk(p["player"].split("/")[0])) if is_utrgv else None
                players_rows.append({"coach_id": cid, "coach_name": c["coach"], "room": ROOM.get(c["coach"], ""), "stop": s["stop"], "tier": tier.upper(),
                    "rank": p.get("rank"), "player": p["player"], "pos": p["pos"], "years": p["years"],
                    "nfl_level": p.get("nfl_level"), "honor_level": p.get("honor_level"),
                    "pff_best_grade": pb.get("grade", ""), "pff_season": pb.get("season", ""), "pff_source": pb.get("source", ""),
                    "recruit_class": pr.get("class_year", ""), "stars_247": pr.get("stars_247", ""), "composite_247": pr.get("composite_247", ""),
                    "stars_rivals": pr.get("stars_rivals", ""), "national_rank_247": pr.get("national_rank_247", ""),
                    "hs_name": pr.get("hs_name", ""), "hs_city": pr.get("hs_city", ""), "hs_state": pr.get("hs_state", ""),
                    "origin": pr.get("origin", ""), "height_signing": pr.get("height_signing", ""), "weight_signing": pr.get("weight_signing", ""),
                    "hs_stats": pr.get("hs_stats", ""), "hs_honors": pr.get("hs_honors", ""),
                    "forty": cb.get("forty", ""), "shuttle": cb.get("shuttle", ""), "vertical": cb.get("vertical", ""), "broad": cb.get("broad", ""), "combine_source": cb.get("source", ""),
                    "recruit_match_status": pr.get("match_status", ""), "recruit_confidence": pr.get("confidence", ""), "recruit_notes": pr.get("notes", ""),
                    "outcome": p["outcome"], "sources": " ; ".join(p["sources"]), "recruit_sources": " ; ".join(pr.get("sources_web", []) + pr.get("source_local", [])),
                    "utrgv_player": "yes" if is_utrgv else "", "cfbd_player_id": cfbd or ""})
                # ---- 2. PlayerFact rows for UTRGV players
                if is_utrgv and not re.search(r"unnamed|none documented|unit outcome", p["player"], re.I):
                    name = p["player"].split(" (")[0]
                    base = {"full_name": name, "cfbd_player_id": cfbd or "", "current_team": TEAM}
                    src = "EDGE3 coaching tree 2026-10-22 (pilot/utrgv/coaching-tree); " + (p["sources"][0] if p["sources"] else "")
                    facts.append({**base, "kind": "coaching_tree", "label": f"{c['coach']} ({ROOM.get(c['coach'],'')}) room, {tier.upper()} #{p.get('rank')}", "value": p["outcome"], "sort": 0, "source": src})
                    arch = c["archetype"][0] if c["archetype"] else ""
                    if arch:
                        facts.append({**base, "kind": "coaching_tree", "label": "Coach archetype this player is read against", "value": arch, "sort": 1, "source": "EDGE3 coaching tree 2026-10-22, archetype read for " + c["coach"]})
                    rsrc = "; ".join(pr.get("sources_web", [])[:3]) or "; ".join(pr.get("source_local", []))
                    k = 0
                    for label, val in [("Recruiting class", pr.get("class_year")), ("247 stars", pr.get("stars_247")), ("247 composite", pr.get("composite_247")),
                                       ("Rivals stars", pr.get("stars_rivals")), ("High school", ", ".join(str(x) for x in (pr.get("hs_name"), pr.get("hs_city"), pr.get("hs_state")) if x not in (None, "", "nan"))),
                                       ("Origin", pr.get("origin")), ("Size at signing", f"{pr.get('height_signing') or '?'}/{pr.get('weight_signing') or '?'}" if (pr.get("height_signing") or pr.get("weight_signing")) else None),
                                       ("HS production", pr.get("hs_stats")), ("HS honors", pr.get("hs_honors")),
                                       ("Testing", f"40 {cb.get('forty')}" + (f" ({cb.get('source')})" if cb.get("source") else "") if cb.get("forty") else None)]:
                        if val not in (None, "", "nan", "None"):
                            k += 1
                            facts.append({**base, "kind": "recruiting_profile", "label": label, "value": str(val), "sort": k, "source": rsrc or "EDGE3 recruiting pass 2026-10-22"})
                    if pr.get("match_status") and "unverified" in str(pr["match_status"]) and "web pass" not in str(pr["match_status"]):
                        facts.append({**base, "kind": "recruiting_profile", "label": "Verification", "value": "Local name match not yet verified; confirm before showing on a coach surface.", "sort": 99, "source": "EDGE3 recruiting pass 2026-10-22"})

def wcsv(name, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# de-dup facts (same player can sit in two rooms, e.g. Box)
seen = set(); facts2 = []
for f in facts:
    key = (f["full_name"], f["kind"], f["label"], f["value"][:80])
    if key in seen: continue
    seen.add(key); facts2.append(f)
wcsv("coaching_tree_coaches.csv", coaches_rows); wcsv("coaching_tree_stops.csv", stops_rows); wcsv("coaching_tree_players.csv", players_rows); wcsv("player_facts_utrgv.csv", facts2)

# ---- 3. System view (New Mexico pattern)
def band(coach_name):
    c = by_coach[coach_name]; tops = [p for s in c["stops"] for p in s["top"]]
    stars = [int(p["recruit_profile"]["stars_247"]) for p in tops if (p.get("recruit_profile") or {}).get("stars_247") not in (None, "")]
    origins = Counter()
    for p in tops:
        o = str((p.get("recruit_profile") or {}).get("origin") or "").lower()
        origins["walk-on" if "walk-on" in o else "JUCO" if "juco" in o else "transfer" if "transfer" in o else "HS" if o.startswith("hs") else "unknown"] += 1
    hw = [(p["recruit_profile"].get("height_signing"), p["recruit_profile"].get("weight_signing")) for p in tops if (p.get("recruit_profile") or {}).get("height_signing")]
    parts = []
    if stars: parts.append(f"{min(stars)} to {max(stars)}★ ({len(stars)} rated of {len(tops)}; {'no 4★' if max(stars) < 4 else 'one 4★+'})")
    om = ", ".join(f"{k} {v}" for k, v in origins.most_common() if k != "unknown")
    if om: parts.append("origin " + om)
    if hw: parts.append("signing size " + ", ".join(f"{h}/{w or '?'}" for h, w in hw[:4]))
    return " · ".join(parts)

def proof(coach_name, n=4):
    c = by_coach[coach_name]; rows = []
    for s in c["stops"]:
        for p in s["top"]:
            if "UTRGV" in s["stop"] or re.search(r"unnamed|group|not Bush", p["player"]): continue
            rows.append((p.get("nfl_level", 0), p.get("honor_level", 0), (p.get("pff_best") or {}).get("grade") or -1, f"{p['player'].split(' (')[0]} ({s['stop'].split(',')[0]}, {p['years']}): {p['outcome'][:110]}"))
    rows.sort(reverse=True)
    return [r[3] for r in rows[:n]]

def pos_room(pos):
    p = str(pos).upper()
    if p.startswith("QB"): return "QB"
    if p.startswith(("RB", "HB")): return "RB"
    if p.startswith("WR"): return "WR"
    if p.startswith("TE"): return "TE"
    if p.startswith(("OL", "OT", "OG", "C ", "C(", "G ")): return "OL"
    if p.startswith(("DE", "EDGE")): return "EDGE"
    if p.startswith(("DL", "NT", "DT")): return "DL"
    if p.startswith(("LB", "ILB", "OLB")): return "LB"
    if p.startswith(("S", "DB", "FS", "SS")): return "S"
    if p.startswith("CB"): return "CB"
    return None

def maps_to(room):
    """2025 UTRGV producers in this room, from any coach's UTRGV stop (Marburger sits under Bush, Box under three coaches)."""
    out, seen = [], set()
    for c in tree["coaches"]:
        for s in c["stops"]:
            if "UTRGV" not in s["stop"]: continue
            for p in s["top"]:
                if re.search(r"unnamed|none documented|unit outcome", p["player"]): continue
                if pos_room(p["pos"]) != room: continue
                name = p["player"].split(" (")[0]
                if name in seen: continue
                seen.add(name)
                pr = p.get("recruit_profile") or {}
                tag = " · ".join(x for x in [f"{pr['stars_247']}★" if pr.get("stars_247") not in (None, "") else ("unrated" if pr.get("match_status", "").endswith("web pass done") else ""), str(pr.get("origin") or "").split(" (")[0], f"{pr.get('height_signing')}/{pr.get('weight_signing') or '?'}" if pr.get("height_signing") else ""] if x)
                out.append(f"{name} ({p['pos'].split(',')[0]}; {tag}): {p['outcome'][:90]}" if tag else f"{name} ({p['pos'].split(',')[0]}): {p['outcome'][:90]}")
    return out

SLOTS = [
 ("QB", "Quarterback", "Theron Aych", "Accurate, moderately mobile processor who can run when needed; converts and late bloomers welcome. Bush's lineage rewards volume passers; Aych's producers spike in year two or three.", "provisional", "Aych is in his first UTRGV season; the room history is Bush's (George, O'Korn, Ward, Marburger) plus Aych's Angelo State and Arizona rooms."),
 ("RB", "Running back", "Marco Regalado", "Downhill, high-floor back in a committee inside a pass-first offense; mature transfers and small Texas HS producers rather than rated recruits.", "provisional", "One UTRGV season of data; Regalado's pre-UTRGV career was personnel, not position coaching."),
 ("WR", "Wide receiver", "Gunnar Henderson", "High-volume, high-TD target who produces young and gets poached upward; small at signing, Texas HS direct.", "provisional", "One season, two producers, both left for FBS. Retention, not evaluation, is the open question."),
 ("TE", "Tight end", "Mike Barela", "Blocking-first tight end with red-zone value, often a Power-5 drop-down or position convert; honors land on the OL when Barela coaches OL.", "ok", "Smith Flores left for ECU; the 2026 room is unproven."),
 ("OL", "Offensive line", "Jeff Bowen", "Durable, high-availability interior players; freshmen who can start and JUCO sophomores who move up within a year. Pass protection is the measured output.", "ok", "Hughes (true freshman All-American), Thompson and Nicklas return; the line protected a Walter Payton finalist."),
 ("DL", "Defensive line", "Nate (Nathan) Langford", "Texas-rooted, non-blue-chip paths: FCS transfer, developmental redshirt, veteran nose. Production in TFL and sacks over size.", "ok", "Entire 2025 DL returns; Langford's HS stops carry 'most improved defense' tags but no individual data."),
 ("EDGE", "Edge / outside linebacker", "James Lockhart IV", "Long 235 to 265 lb stand-up/hand-down hybrid; bounce-back transfer rather than rated recruit (Box; Wilson by association at Texas Tech).", "provisional", "One season of Lockhart's own coaching; Box is shared between the OLB and DL rooms."),
 ("LB", "Inside linebacker", "Brian Gamble", "High-volume tackler from an overlooked origin (walk-on, transfer down, true freshman) who plays early in a multiple or 3-4 front.", "ok", "Haygood (102 tackles as a redshirt freshman) is the archetype in the building; Gamble's only documented LOW was a producer who transferred up."),
 ("S", "Safety / nickel", "Adrian McDonald", "Ball-production safety who mirrors McDonald's own 17-INT profile; first-year players on the field; nickel/star versatility.", "ok", "Prosser (Freshman All-American), Graham (NFL draft declare), Hudgens and Neal all transfers or unrated HS; no LOW documented."),
 ("CB", "Cornerback / special teams", "Josh Jones", "Takeaway and pass-breakup volume over size; JUCO and small-school Southern origins; proven in a 4-3 at the FCS/G5 level.", "provisional", "Jones joined in February 2026; no UTRGV corner has been coached by him through a season yet."),
]
bush = by_coach["Travis Bush"]
system = {
 "meta": {"program": "UTRGV Football", "team_short": "UTRGV", "mascot": "Vaqueros", "head_coach": "Travis Bush", "season": 2026,
          "generated": "2026-10-22", "model_note": "Coaching-tree archetypes are priors built from each coach's own history (Rule 1). They are not model output and never carry a R/Y/G tier. Coach workbook names outrank them.",
          "source": "pilot/utrgv/coaching-tree (Edge3-demos branch claude/utrgv-coaching-tree-history-hp4dlh)"},
 "coach": {"name": "Travis Bush", "title": "Head Coach", "prior_program": "First-time college head coach. Assistant stops: Texas State (WR, then associate HC and co-OC, 2004-09), UTSA (first OC, 2011), Houston (RB, then OC/QBs and assistant HC, 2012-14), Buffalo Bills (offensive assistant, 2015); HC at Seguin HS and New Braunfels Canyon HS.",
           "philosophy_quote": None, "philosophy_source": None,
           "system_summary": "A pass-leaning spread with Air Raid influence (Levine/Meacham at Houston) layered on the Texas State offense he helped run to 4th in FCS scoring in 2008. His best players were volume pass-game producers and accurate, moderately mobile quarterbacks; his documented lows were pocket quarterbacks in year two of a system. 2025 synthesized it: a portal QB (Newcomer of the Year), a freshman WR (Freshman of the Year), a freshman OL All-American, 9-3.",
           "system_pillars": [{"label": b.split(":")[0].strip(" *"), "detail": b.split(":", 1)[1].strip() if ":" in b else b} for b in bush.get("hc_archetype", [])[:5]],
           "tree_roots": ["Texas State 2004-10 (Bush, Bowen, Barela, Langford, Regalado)", "UTSA 2011 (Bush, Bowen)", "Houston 2012-14 (Bush; McDonald played)", "Seguin HS 2016-20 (Bush, Langford; Ian Box)", "Spavital node (Gamble, McDonald)", "Meacham node (Bush 2013, Aych 2025)"]},
 "archetype": {"title": "How you play, your program archetype", "lede": "Built from every stop of your career and your position coaches' careers, not from one UTRGV season. Each room below reads the coach's own producers and the recruits they came in as.",
               "system_profile": "Pass-first spread (39.6 ppg in 2025) protected by a developmental line, with a multiple, 3-4-hybrid defense that led the Southland in five categories. Producers across the staff were three-stars and below, Texas-rooted, and arrived from high school, JUCO or as transfers down.",
               "slots": []}}
for abbr, name, coach, arch, status, note in SLOTS:
    system["archetype"]["slots"].append({"abbr": abbr, "slot": name, "coach": coach, "coach_title": by_coach[coach]["utrgv_title"],
        "archetype": arch, "baseline": band(coach) or "no rated producers on record",
        "baseline_note": "Recruiting band of this coach's documented producers across every stop (all positions he coached), from Rule 4; not a model threshold.",
        "tree_proof": proof(coach), "maps_to": maps_to(abbr),
        "y2_status": status, "y2_note": note, "confidence": by_coach[coach].get("confidence", ""), "read_rule": "Coach history, not program history; ranked NFL, then production, then PFF; recruiting profile on every row."})
system["archetype"]["gaps_summary"] = "Combine and camp testing is almost absent from the public record (one hand-timed 40). Recruiting ratings exist for 38 of 100 rows; the rest are unrated by the services, which is itself part of the archetype. Position coaches new in 2026 (Aych, Jones) and one-season rooms (Henderson, Regalado, Lockhart) are provisional until 2026 results land."
(OUT / "system_view_utrgv.json").write_text(json.dumps(system, indent=2, ensure_ascii=False))
print(f"coaches={len(coaches_rows)} stops={len(stops_rows)} players={len(players_rows)} utrgv_with_cfbd_id={sum(1 for r in players_rows if r['cfbd_player_id'])} facts={len(facts2)} slots={len(system['archetype']['slots'])}")
