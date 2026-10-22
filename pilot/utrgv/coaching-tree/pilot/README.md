# Coaching tree, live-pilot package (UTRGV)

Target: the EDGE3 platform Dennis runs for the UTRGV pilot (`edge3-model/platform`, Prisma on Postgres, Cognito sign-in, `edge3_loader` writes reference tables, `edge3_app` reads them). Everything here is league-wide reference built from public and licensed sources, never from UTRGV's private input, so it follows the same RLS-off pattern as `Player`, `PlayerScore`, `PlayerComparable` and `PlayerFact`.

## Files

| File | Loads into | Rows | Notes |
|---|---|---|---|
| `migration_coach_tree.sql` | new Prisma migration (`npm run db:migrate`, name it `coach_tree`) | 3 tables | `CoachStaff`, `CoachStop`, `CoachTreePlayer`; grants mirror `PlayerComparable`. Add the matching models to `schema.prisma` (field names are the camelCase of the CSV headers). |
| `coaching_tree_coaches.csv` | `CoachStaff` | 11 | `coach_id` is the key. Set `program` = `UT Rio Grande Valley`, `season` = 2026 on load. |
| `coaching_tree_stops.csv` | `CoachStop` | 108 | Career timeline per coach, oldest first, with who they worked under and the source URLs. |
| `coaching_tree_players.csv` | `CoachTreePlayer` | 100 | One row per TOP or LOW player per stop, ranked (NFL, production, PFF) with the recruiting profile. `cfbd_player_id` is filled for UTRGV rows so the loader can set `playerId`; historical rows at other schools stay unresolved by design. |
| `player_facts_utrgv.csv` | `PlayerFact` | see build log | Two kinds. `coaching_tree`: which coach's room the player is read in, his rank there, and the archetype he is read against. `recruiting_profile`: class, stars, composite, high school, origin, size at signing, HS production and honors, testing. Resolve `playerId` by `cfbd_player_id`, falling back to `full_name` + `current_team`. |
| `system_view_utrgv.json` | the System view (New Mexico demo pattern: `meta`, `coach`, `archetype.slots[]`) | 10 slots | Head-coach block for Bush, then one slot per room with the position coach, the archetype line, the recruiting baseline band, `tree_proof` (top historical producers), `maps_to` (2025 UTRGV producers), `y2_status` and `y2_note`. |

## Rules the data carries

1. **Coach history, not program history.** Every archetype is built from the coach's own stops. Program-level history is context only. The head coach is read through his assistant stops because UTRGV is his first college head job.
2. **Ranked lists.** Within each stop, TOP and LOW rows are sorted by `nfl_level` desc, then `honor_level` desc, then `pff_best_grade` desc. `rank` is that order. LOW rows exist only where a source documents the outcome; never train on them.
3. **Recruiting profile on every row.** `stars_247`, `composite_247`, class, high school, origin, size at signing, HS stats and honors, testing. `recruit_match_status` says whether a local name match was verified; `recruit_confidence` is the web pass's own rating. Blanks are blanks, not zeros.
4. **Provenance.** `sources` and `recruit_sources` hold the URLs behind the row. Unverified stays labeled.

## Vocabulary

- These rows are **facts and priors**, never `coach_notes` (reserved for real coach prose) and never a model tier. Nothing here carries a Red/Yellow/Green read.
- "Baseline" on the System view means the coach's standard, consistent with the 10-11 brief. When a trend is unavailable the label stays "Trend builds this season."
- When Cam's Positional Baseline Workbook returns the coach's own two names per position, those names outrank `tree_proof`. Where they disagree, flag for the coach rather than average.

## Load order

1. Run the migration and add the three models to `schema.prisma`; `npm run db:verify` should count 21 tables and the new grants.
2. Load `coaching_tree_coaches.csv`, then `_stops.csv`, then `_players.csv` on the `edge3_loader` connection (CSV `coach_id` → `CoachStaff.id`; generate `id` for stops and players with cuid like the other loaders).
3. Resolve `CoachTreePlayer.playerId` and `PlayerFact.playerId` for UTRGV rows via `Player.cfbdPlayerId`, else `Player.fullName` + `Player.currentTeam = 'UT Rio Grande Valley'`.
4. Load `player_facts_utrgv.csv` into `PlayerFact` (kind, label, value, sort, source as given).
5. Point the System view at `system_view_utrgv.json`; `archetype.slots[].maps_to` names resolve the same way as step 3.

## Known limits

- PFF grades joined for FBS stops 2014 to 2025 only; UTRGV 2025 PFF (FCS pull in Drive) is the next join.
- Testing data is nearly absent in the public record (one hand-timed 40). Treat `forty`, `shuttle`, `vertical`, `broad` as sparse by nature.
- Three one-season rooms (WR, RB, EDGE) and two coaches new in 2026 (QB, CB) are marked `provisional` on the System view.
- Two Texas State linebackers were removed from Gamble's room after the recruiting pass showed they arrived after his tenure; the correction is noted on that stop.
