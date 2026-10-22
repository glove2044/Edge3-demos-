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

def recruit(p):
    r = p.get("recruit_profile") or {}
    if not any(r.get(k) not in (None, "") for k in ("stars_247", "composite_247", "hs_name", "height_signing", "origin")):
        return ""
    bits = []
    if r.get("stars_247") not in (None, ""):
        bits.append(f"{r['stars_247']}★" + (f" {r['composite_247']:.4f}" if isinstance(r.get("composite_247"), (int, float)) else ""))
    elif isinstance(r.get("composite_247"), (int, float)):
        bits.append(f"{r['composite_247']:.4f}")
    if r.get("class_year"):
        bits.append(f"class {r['class_year']}")
    hs = ", ".join(str(x) for x in (r.get("hs_name"), r.get("hs_city"), r.get("hs_state")) if x not in (None, "", "nan"))
    if hs:
        bits.append(hs)
    if r.get("height_signing") or r.get("weight_signing"):
        bits.append(f"{r.get('height_signing') or '?'}/{r.get('weight_signing') or '?'}")
    if r.get("origin"):
        bits.append(str(r["origin"]))
    cb = r.get("combine") if isinstance(r.get("combine"), dict) else {}
    tests = [f"40 {cb['forty']}" if cb.get("forty") else "", f"SH {cb['shuttle']}" if cb.get("shuttle") else "",
             f"VJ {cb['vertical']}" if cb.get("vertical") else "", f"BJ {cb['broad']}" if cb.get("broad") else ""]
    tests = [t for t in tests if t]
    if tests:
        bits.append("; ".join(tests) + (f" ({cb['source']})" if cb.get("source") else ""))
    if r.get("hs_stats"):
        bits.append(f"HS: {r['hs_stats']}")
    st = str(r.get("match_status", ""))
    if "unverified" in st and "web pass" not in st:
        bits.append("[unverified match]")
    return " · ".join(bits)

def table(rows, last_col):
    if not rows:
        return "not found\n"
    s = f"| # | Player | Pos | Years | NFL | Production | PFF best | Recruiting / HS profile | {last_col} | Source |\n|---|---|---|---|---|---|---|---|---|---|\n"
    for p in rows:
        s += f"| {p['rank']} | {p['player']} | {p['pos']} | {p['years']} | {NFL.get(p['nfl_level'], '')} | {PROD.get(p['honor_level'], '')} | {pff(p)} | {recruit(p)} | {p['outcome']} | {src(p['sources'])} |\n"
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
