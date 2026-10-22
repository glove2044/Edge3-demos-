#!/usr/bin/env python3
"""Parse the per-coach dossier markdown files into coaching_tree.json and two CSVs."""
import csv, json, re, sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

FILES = sorted(SRC.glob("0*.md"))

coaches = []
coach = None
stop = None
mode = None          # 'timeline' | 'top' | 'low' | None
section = None       # 'tree' | 'archetype' | 'confidence' | 'gaps' | None

def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells

def is_sep(cells):
    return all(re.fullmatch(r":?-{2,}:?", c) for c in cells)

def urls(text):
    return re.findall(r"https?://[^\s;)|]+", text)

for f in FILES:
    for raw in f.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("### ") and not line.startswith("#### "):
            name, _, title = line[4:].partition(" — ")
            coach = {"coach": name.strip(), "utrgv_title": title.strip(), "source_file": f.name,
                     "timeline": [], "mentors": [], "stops": [], "archetype": [],
                     "confidence": "", "gaps": "", "notes": []}
            coaches.append(coach)
            stop = None; mode = None; section = None
            continue
        if coach is None:
            continue
        if line.startswith("#### "):
            stop = {"stop": line[5:].strip(), "top": [], "low": [], "notes": []}
            coach["stops"].append(stop)
            mode = None; section = None
            continue
        if line.startswith("**Timeline**"):
            mode = "timeline"; section = None; continue
        if line.startswith("**Tree / mentors**"):
            section = "tree"; mode = None; continue
        if line.startswith("**Players by stop**"):
            section = None; mode = None; continue
        if line.startswith("**Archetype read**"):
            section = "archetype"; mode = None; continue
        if line.startswith("**Confidence**"):
            coach["confidence"] = line.replace("**Confidence**:", "").strip(); section = None; mode = None; continue
        if line.startswith("**Gaps**"):
            coach["gaps"] = line.replace("**Gaps**:", "").strip(); section = None; mode = None; continue
        if line.startswith("**What Bush"):
            section = "hc_archetype"; coach.setdefault("hc_archetype", []); mode = None; continue
        if re.match(r"^TOP:?", line):
            mode = "top"
            rest = line[4:].strip()
            if rest and stop is not None:
                stop["notes"].append("TOP: " + rest)
            continue
        if re.match(r"^LOW:?", line):
            mode = "low"
            rest = line[4:].strip()
            if rest and stop is not None:
                stop["notes"].append("LOW: " + rest)
            continue
        if line.startswith("|"):
            cells = split_row(line)
            if is_sep(cells) or cells[0] in ("Years", "Player"):
                continue
            if mode == "timeline" and len(cells) >= 5:
                coach["timeline"].append({"years": cells[0], "school": cells[1], "role": cells[2],
                                          "worked_under": cells[3], "sources": urls(cells[4])})
            elif mode in ("top", "low") and stop is not None and len(cells) >= 5:
                stop[mode].append({"player": cells[0], "pos": cells[1], "years": cells[2],
                                   "outcome": cells[3], "sources": urls(cells[4])})
            continue
        if line.startswith("- ") and section == "tree":
            coach["mentors"].append(line[2:].strip()); continue
        if line.startswith("- ") and section == "archetype":
            coach["archetype"].append(line[2:].strip()); continue
        if line.startswith("- ") and section == "hc_archetype":
            coach["hc_archetype"].append(line[2:].strip()); continue
        if line.strip() and stop is not None and mode in ("top", "low", None) and not line.startswith("**"):
            stop["notes"].append(line.strip()); continue
        if line.strip() and stop is None and section is None and mode is None and not line.startswith("**") and not line.startswith("---") and not line.startswith("("):
            coach["notes"].append(line.strip())

# Flatten players
players = []
for c in coaches:
    for s in c["stops"]:
        for tier in ("top", "low"):
            for p in s[tier]:
                players.append({"coach": c["coach"], "utrgv_title": c["utrgv_title"], "stop": s["stop"],
                                "tier": tier.upper(), "player": p["player"], "pos": p["pos"],
                                "years": p["years"], "outcome": p["outcome"], "sources": " ; ".join(p["sources"])})
timeline = []
for c in coaches:
    for t in c["timeline"]:
        timeline.append({"coach": c["coach"], "utrgv_title": c["utrgv_title"], "years": t["years"],
                         "school": t["school"], "role": t["role"], "worked_under": t["worked_under"],
                         "sources": " ; ".join(t["sources"])})

meta = {"program": "UTRGV Football", "season": 2026, "prepared_for": "EDGE3 UTRGV pilot (Dennis Livshyts)",
        "prepared_on": "2026-10-22", "method": "Web research from official school bios, conference releases and news; every row carries source URLs. Items marked unverified or not found could not be confirmed.",
        "coach_count": len(coaches), "player_rows": len(players), "timeline_rows": len(timeline)}
(OUT / "coaching_tree.json").write_text(json.dumps({"meta": meta, "coaches": coaches}, indent=2, ensure_ascii=False), encoding="utf-8")
with (OUT / "coaching_tree_players.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(players[0].keys())); w.writeheader(); w.writerows(players)
with (OUT / "coaching_tree_timeline.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(timeline[0].keys())); w.writeheader(); w.writerows(timeline)
print(json.dumps(meta, indent=2))
for c in coaches:
    print(f"{c['coach']:<22} timeline={len(c['timeline']):>2} stops={len(c['stops'])} top={sum(len(s['top']) for s in c['stops'])} low={sum(len(s['low']) for s in c['stops'])} mentors={len(c['mentors'])} arche={len(c['archetype'])}")
