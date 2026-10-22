# Paste block for edge3-model/CLAUDE.md

Insert after the "📐 MODELING PRINCIPLE (2026-05-22, Kenyon) — don't proxy missing data" section. This session had read-only access to edge3-model, so the block is provided here rather than pushed.

---

## 🌳 COACHING TREE PRINCIPLE (2026-10-22, Kenyon) — coach history, not program history

Position baselines, archetypes and comps are built from the **coach's own history at every stop**, not the program's pooled history. Program history is context only. A first-time head coach (Bush at UTRGV) is read through his assistant stops. Staff-history source order: official bio → prior-school bios → **team media guides** (the only reliable source for OC/DC/position-coach assignments by year) → conference releases → press. CFBD covers FBS head coaches only; assistant and FCS histories need their own source (`data/fcs/fcs_head_coaches_manual.csv` is the start of that layer).

**Position coach → player mapping, ranked.** Every position coach maps to the players he coached at each stop, as TOP and LOW lists, both sorted highest to lowest by: (1) NFL outcome (drafted / roster / honors > UDFA / camp / other pro > none), (2) production (All-American or POY > 1st team > 2nd team or newcomer/FOY > HM, 3rd team, all-region, academic > records or team-leading > stats), (3) best PFF season grade during the coach's years at that stop (`edge3-pff-integration/data/pff/ncaa/*_2014_2025.csv`, matched on player + team + position group). A player is LOW only when a source documents the outcome. Never train on the LOW set.

**Provenance.** Every row carries its source URL; unverified stays labeled; source disagreements are reported, not resolved silently.

Reference implementation and the UTRGV 2026 staff tree: `Edge3-demos/pilot/utrgv/coaching-tree/` (branch `claude/utrgv-coaching-tree-history-hp4dlh`): `coaching_tree.json`, `coaching_tree_players.csv`, `dossiers/parse_tree.py`, `dossiers/rank_players.py`. The comps script `scripts/build_utrgv_fcs_comps.py` already applies the coach-history rule to comp selection (`BUSH_TREE` rooms first).
