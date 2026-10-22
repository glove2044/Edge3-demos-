# Edge3-demos — Working Context

Static demo site for EDGE3 (Netlify publishes the repo root, no build step). The `pilot/` folder holds pilot work product that is not part of the public site; keep it on a branch or move it out before merging to `main`, because Netlify publishes every file at the root.

## Coaching tree rules (Kenyon, 2026-10-22)

These apply to every coach baseline, position archetype and comp set EDGE3 builds. Full text: `pilot/utrgv/coaching-tree/RULES.md`. The same block belongs in the edge3-model `CLAUDE.md` next to the modeling principles.

1. **Coach history, not program history.** Baselines come from the coach's own career at every stop, not the program's pooled history. A first-time head coach is read through his assistant stops. Staff-history sources in order: official bios, prior-school bios, team media guides (the only reliable source for OC, DC and position-coach assignments by year), conference releases, press. CFBD covers FBS head coaches only.
2. **Map every position coach to the players he coached, ranked.** TOP and LOW lists per stop, both sorted highest to lowest by NFL outcome first, then production (All-American or POY, first team, second team or newcomer of the year, HM or third team, records or team-leading, stats), then PFF grade (best season grade in the coach's years at that stop, matched by player, team and position group). LOW only when a source documents the outcome. Never train on LOW.
3. **Match every mapped player to his recruiting profile.** 247Sports Composite (with Rivals and On3 where they differ), class year and commit school; high school, city, state, height and weight at signing, HS production and honors from MaxPreps or press, origin (HS, JUCO, transfer down, walk-on); combine or camp testing with the event named. Local tables first (edge3-model 247 proxy, CFBD recruits), then the web. Same-name matches count only when the commit school or high school agrees with the player's path. Blanks stay blank; never estimate a rating or a 40 time.
4. **Every row carries its source.** Unverified stays labeled unverified. Source disagreements are reported, not resolved silently.

## Pilot artifacts

- `pilot/utrgv/coaching-tree/` — UTRGV staff coaching tree (report, PDF, JSON, CSVs, source dossiers, parser and ranking scripts).
