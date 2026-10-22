#!/usr/bin/env python3
"""Render the ranked coaching_tree.json back into per-coach dossier markdown (ranked tables)."""
import json, sys
from pathlib import Path

tree = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2])

NFL = {3: "NFL", 2: "Pro (UDFA/other)", 0: ""}
PROD = {6: "6 AA/POY", 5: "5 1st team", 4: "4 2nd team/FOY", 3: "3 HM/3rd", 2: "2 record/led team", 1: "1 stats", 0: ""}

def src(urls):
    return " ; ".join(urls) if urls else "not found"

def pff(p):
    b = p.get("pff_best")
    return f"{b['grade']:.1f} ({b['season']} {b['source']})" if b else ""

def table(rows, last_col):
    if not rows:
        return "not found\n"
    s = f"| # | Player | Pos | Years | NFL | Production | PFF best | {last_col} | Source |\n|---|---|---|---|---|---|---|---|---|\n"
    for p in rows:
        s += f"| {p['rank']} | {p['player']} | {p['pos']} | {p['years']} | {NFL.get(p['nfl_level'], '')} | {PROD.get(p['honor_level'], '')} | {pff(p)} | {p['outcome']} | {src(p['sources'])} |\n"
    return s

parts = []
for c in tree["coaches"]:
    md = [f"### {c['coach']} — {c['utrgv_title']}", ""]
    if c.get("notes"):
        md += [" ".join(c["notes"]), ""]
    md += ["**Timeline**", "", "| Years | School | Role | Worked under (HC / coordinator) | Source |", "|---|---|---|---|---|"]
    for t in c["timeline"]:
        md.append(f"| {t['years']} | {t['school']} | {t['role']} | {t['worked_under']} | {src(t['sources'])} |")
    md += ["", "**Tree / mentors**", ""] + [f"- {m}" for m in c["mentors"]] + [""]
    md += ["**Players by stop** (ranked: NFL, then production, then PFF; highest to lowest)", ""]
    for s in c["stops"]:
        md += [f"#### {s['stop']}", "", "TOP:", "", table(s["top"], "Honor / outcome"), "LOW:", "", table(s["low"], "What happened")]
        for n in s.get("notes", []):
            if n.startswith("TOP:") or n.startswith("LOW:"):
                n = n[4:].strip()
            if n and n not in ("not found", "not found.", "none documented", "none documented."):
                md.append(n + "\n")
    md += ["**Archetype read**", ""] + [f"- {a}" for a in c["archetype"]] + [""]
    if c.get("hc_archetype"):
        md += ["**What Bush's own tree says about his HC archetype**", ""] + [f"- {a}" for a in c["hc_archetype"]] + [""]
    md += [f"**Confidence**: {c['confidence']}", "", f"**Gaps**: {c['gaps']}", "", "---", ""]
    parts.append("\n".join(md))
out.write_text("\n".join(parts), encoding="utf-8")
print("rendered", len(tree["coaches"]), "coaches ->", out)
