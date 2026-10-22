# UTRGV Football Coaching Tree History

**EDGE3 · UTRGV Recruiting Intelligence Pilot · prepared for Dennis Livshyts · October 22, 2026**

## Why this exists

The UTRGV pilot reads every recruit against the coach's own standard, not a national average. The position archetypes come from two inputs: what the staff tells Cam in the Positional Baseline Workbook, and what each coach's history says about the players who produced for him and the players who did not. This document is the second input: the coaching tree for Head Coach Travis Bush and every position coach on the 2026 staff, with the top-performing and low-performing players at each stop where a tree could be mapped.

Coach Bush is a first-time college head coach, so his tree goes back to every stop where he was an assistant (Texas State, UTSA, Houston, Buffalo Bills) and his two Texas high school head-coaching jobs. The same method is applied to the ten position coaches.

Dennis's October 9 summary referenced "the tree designed for Coach Bush" as the template for coaching-tree data in the model. That earlier artifact could not be located in the Edge3-demos repo, Google Drive, Gmail, or the cloud sessions searchable from this environment, so this is a fresh run. If the original turns up on the desktop, treat this document as the superset and reconcile the two.

## Method and limits

- Sources: official school bios, conference all-conference releases, NFL and UFL team releases, Wikipedia season pages, and regional press (Texas Football, RGV Sports, KRGV, Tucson.com and others). Every timeline row and every player row carries its source URLs.
- Rule for LOW performers: a player is listed as LOW only when a source documents the outcome (benched, transferred out after a down year, "expected breakout" that did not happen). No player is called low on judgment alone. That rule keeps the LOW set small and honest. It is thin on purpose.
- Direct page fetches failed from this environment (goutrgv.com, school sites and Wikipedia did not resolve), so every fact comes from search-result excerpts of the cited pages. Anything marked "unverified" or "not found" should be confirmed on the page before it is used in a coach-facing surface.
- FCS, Division II, JUCO and high school stops have little public honors coverage. Where a stop says "thin," the gap is in the public record, not in the coach.

## Ranking rule for the player lists

Within each stop, the TOP and LOW lists are sorted highest to lowest by the same key: NFL outcome first, production second, PFF grade third.

| Column | Values |
|---|---|
| NFL | NFL (drafted, NFL roster, or NFL honors) ranks above Pro (undrafted free agent, camp, practice squad, Arena/CFL/UFL), which ranks above blank. The Bills 2015 room is NFL by definition. |
| Production | 6 All-American or conference/national player of the year · 5 first-team all-conference · 4 second team, newcomer, freshman or rookie of the year · 3 honorable mention, third team, all-region or academic · 2 school record or team-leading production · 1 stats only |
| PFF best | Best PFF season grade during the coach's years at that stop, matched on player, team and position group, from the licensed PFF NCAA tables in edge3-model (FBS, 2014 to 2025). Blank at FCS, D2, JUCO, high school and pre-2014 stops is expected. 26 of 103 player rows carry a PFF grade. |

The three levels are stored on every player row in `coaching_tree.json` and `coaching_tree_players.csv` (`nfl_level`, `honor_level`, `pff_best`), so the sort can be re-run or changed in code.

## The 2026 staff and where each tree roots

| Coach | 2026 title | Tree roots | Years as position coach or coordinator | Timeline confidence | Player-list confidence |
|---|---|---|---|---|---|
| Travis Bush | Head Coach | Texas State (Bailiff, Wright), UTSA (Coker), Houston (Levine, Meacham), Bills (Ryan, Roman, Lynn) | 2004 to present | Medium-High | Medium |
| Brian Gamble | Asst. HC, Defensive Coordinator, LB | Texas A&M (Slocum, as player), Incarnate Word (Santiago, Kennan), Louisiana Tech (Holtz), Texas State (Spavitals) | 2004 to present | Medium | Low-Medium |
| Jeff Bowen | Co-OC, Offensive Line | Texas State (played for Bush-era staff), UTSA (Coker, Bush), Northwestern State, NEO A&M, SFA, Northeastern State | 2014 to present | Medium | Low |
| Theron Aych | Co-OC, Quarterbacks (play-caller) | Angelo State (Wagner), UTEP (Kugler), Arizona (Rodriguez, Sumlin), Tennessee State (George), Oklahoma State (Gundy, Meacham) | 1997 to present | Medium | Low-Medium |
| Adrian McDonald | Pass Game Coordinator, Safeties | Houston (played under Levine while Bush was OC; Zac Spavital his DB coach), Texas State (Spavitals), Midwestern State | 2018 to present | High | Low |
| Gunnar Henderson | Pass Game Coordinator, Wide Receivers | UTRGV only (Bush); played at UIW (Morris) and TCU (Patterson, Dykes) | 2024 to present | High | Medium-Low |
| Mike Barela | Run Game Coordinator, Tight Ends | Texas State (Wright, with Bush), Northeastern State (Evans), UIW (Kennan), Colorado Mesa and Valdosta State (Jackson) | 1996 to present | Medium-High | Medium |
| Marco Regalado | Running Backs, Recruiting Coordinator | Rice personnel (Bloomgren), Washington State recruiting, Jaguars fellowship; one HS RB season before UTRGV | 2020 to present (on-field) | Medium | Low-Medium |
| James Lockhart IV | Outside Linebackers | Baylor and Texas Tech (Joey McGuire, C.J. Ah You, DeRuyter) | 2024 to present | High | Low |
| Nate Langford | Defensive Line | Texas State (played under Bush-era staff), Seguin HS (Bush's DC), Luling HS (HC) | 2016 to present | Medium | Low |
| Josh Jones | Special Teams Coordinator, Cornerbacks | Henderson State (Maxfield), Central Arkansas and South Alabama (Campbell, Stewart), Brahmas (Wade Phillips) | 2015 to present | High | Medium (UCA, South Alabama), Low elsewhere |

## How the staff connects: shared nodes in the tree

The staff is not eleven separate trees. It is one tree with a few trunks, and that matters for the archetype: the same offensive lineage is being applied by several coaches at once.

1. **Texas State, 2004 to 2010 (the trunk).** Bush coached WRs then was associate head coach and co-OC under Brad Wright. Bowen played center on that offense (2008 first-team All-Southland). Langford played DE for the same program while Bush was on staff. Barela coached tight ends and ran operations next to Bush from 2007 to 2010. Regalado is a Texas State graduate. Five of eleven staff members share this root.
2. **UTSA, 2011 (the start-up).** Bush was the first offensive coordinator; Bowen was an offensive GA on the same inaugural staff. Bush has said publicly that UTSA's start-from-scratch build is the blueprint for UTRGV.
3. **Houston, 2012 to 2014.** Bush was running backs coach, then play-caller and assistant head coach under Tony Levine. McDonald was the starting safety on those teams and set the school interception record. Doug Meacham was Bush's co-OC in 2013 and was Aych's offensive coordinator at Oklahoma State in 2025, which is the one scheme bridge between Bush and his new play-caller.
4. **Seguin High School, 2016 to 2020.** Bush was head coach, Langford was his defensive coordinator, and UTRGV's best 2025 pass rusher, Ian Box, is a Seguin product.
5. **The Spavital node.** Zac Spavital coached McDonald at Houston and brought him to Texas State as a GA; Gamble coached inside linebackers on the same Texas State staff in 2021 and 2022. Gamble's 2022 unit was credited with the best defensive production in Texas State's FBS history.
6. **Incarnate Word.** Gamble spent ten years there (DL coach, then defensive coordinator); Barela coached tight ends and the run game there in 2015 to 2017; Henderson played there in 2018 and 2019.

Outliers with their own trees: Aych (South Dakota, JUCO, Angelo State, Arizona, Tennessee State, Oklahoma State), Lockhart (Baylor and Texas Tech, Joey McGuire), Jones (Arkansas and Alabama FCS/G5 circuit, then the UFL).

## Cross-staff archetype summary

Each line is built only from the documented players in the dossiers that follow. Read it as a prior for the position baseline, not as a label on any recruit.

| Position group | Coach | What the top performers had in common | Where the pattern broke (documented LOW) |
|---|---|---|---|
| Offense, program-wide | Bush | Volume pass-game producers: record-setting WRs (Luke 17 TD, Greenberry 100 ypg), accurate and moderately mobile QBs (George 63%, Marburger 31 TD, Ward as a converted athlete). Mostly Texas HS products or Texas-college transfers; honors came as often from lightly recruited players as from blue-chips. | Both documented lows are pocket QBs in year two of a system who lost the job to a more mobile replacement (Piland 2012, O'Korn 2014). Projection risk is highest at drop-back QB after a staff or scheme change. |
| Quarterback | Aych | Oversized or athletically unusual converts and dual-threat producers (Washington 3,691 pass and 831 rush yds; Walker WR-to-NFL TE; Poindexter 6-5 late bloomer). Low-pedigree origins: D2, JUCO, walk-on. Production spikes in year two or three, not year one. | Lows cluster around staff churn (Arizona 2020, Tennessee State 2022) rather than misreads; Curry is the one "expected breakout" that did not produce. |
| Wide receiver | Henderson | One season of data. Both top producers were young (Diaz a true freshman), high-TD, and left for FBS within a year. The room exports talent. | None documented. The retention problem is upward, not downward. |
| Offensive line | Bowen | Young and developmental (Hughes all-conference as a true freshman), a JUCO-to-FBS track record (four of five NEO sophomores signed FBS), durability and availability (Wrather 24 straight starts). Pass protection is the measured output. | None documented. |
| Tight end and run game | Barela | Power-5 drop-down transfers and position converts (Bowie, Smith Flores). Blocking-first TEs with red-zone value (Smith Flores 20 catches, 6 TD). Honors land on the OL when he coaches OL. | None documented; only upward departure (Smith Flores to ECU). |
| Running back | Regalado | One season of data. Lead back was a mature graduate transfer (Denney, Yale) in a committee inside a pass-first offense; stated philosophy is downhill. Sourcing leans on the portal (Denney, Lane from LSU for 2026). | None documented. |
| Defense, program-wide and LB | Gamble | High-volume tacklers over rated recruits (Grubbs 99, Baldwin 85, Haygood 102). Overlooked origins: walk-on, FBS transfer down, true freshman at a start-up. Plays young ILBs early. Multiple and 3-4 fronts ask ILBs to stack tackles. | The one documented low (Foster) was a productive starter who transferred up to Louisville. The failure mode is retention of producers, not evaluation. |
| Outside linebacker and edge | Lockhart | Long 235 to 265 lb edge rushers used as stand-up/hand-down hybrids (Box; Wilson by association at Texas Tech). Texas HS products arriving as bounce-back transfers rather than rated recruits. | None documented (one season). |
| Defensive line | Langford | Texas-rooted, non-blue-chip paths: FCS transfer (Box), developmental redshirt producing as a rotational sub (Anderson), veteran grad-transfer nose (Huerta). Every HS stop carries a "most improved defense" tag. | None documented (one season). |
| Safeties | McDonald | Ball-production players who mirror McDonald's own 17-INT profile (Prosser pick-six, Graham All-American buzz). First-year players on the field (Davis, Prosser). Nickel/"star" versatility. | None documented. |
| Cornerbacks and special teams | Jones | Takeaway and pass-breakup volume over size (Smith 10 INT/37 PD, Thompson 9 INT, Williams nation-leading PBU claim). JUCO and small-school Southern origins. All documented production came in a Campbell/Stewart 4-3 at FCS/G5 level. | None documented. |

Two staff-wide signals stand out. First, almost every documented top performer was lightly recruited, a transfer down, a walk-on, or a true freshman; blue-chip high school recruits are rare in every tree. Second, where lows exist at all, they are either pocket QBs after a scheme change or productive players who transferred up. The staff's historical risk is losing its best players to FBS, not misjudging them.

## How to use this in the pilot

- `coaching_tree.json` holds the full structure: for each coach, the timeline (years, school, role, who they worked under, sources), mentors, archetype bullets, confidence, gaps, and each stop with TOP and LOW player rows. `coaching_tree_players.csv` and `coaching_tree_timeline.csv` are the flattened versions.
- The archetype bullets are priors for the position baseline that Cam collects in the workbook. When the coach names his own two players per position, those names outrank this document. Where the coach's names and this history agree, the archetype is strong; where they disagree, flag it for the coach rather than averaging.
- Do not train on the LOW set. It is too small and too dependent on staff churn to carry signal. Use it as a list of documented failure modes to check a recruit against (pocket QB in a new system, producer likely to be poached upward).
- Mentor names and schemes are the join keys to the model's existing coaching data (CFBD covers FBS head coaches only). Assistant and FCS histories in this document are the part CFBD does not have.

## Chase Ames: what was pulled, and what Coach Bush received

Chase Ames is a 2027 quarterback from Dripping Springs High School (Texas Class 6A). He is the recruit whose read was built on Coach Bush's own history rather than UTRGV's one-season program history, and that method is now Rule 1 below. The record, from Gmail, Drive and the edge3-model repo:

| Date | What | Where it lives |
|---|---|---|
| June 12, 2026 | Ames family check-in (Chase, Matt Ames, Brian, Kenyon). The decision was a pivot to targeting specific coaching systems and downstream schools with a clear path to playing time, instead of star-based rankings. | Drive: "Ames Family Edge3 Check in, 2026/06/12, Notes by Gemini" |
| July 13, 2026 | Brian sent Chase and Matt a personalized UTRGV visit guide for the July 14 visit, with the questions to ask on the visit. | Email "UTRGV/ Chase Ames"; page amesutrgv.netlify.app |
| July 13, 2026 | Brian sent Coach Bush the UTRGV Risk/Fit wallet on Chase "and how he maps to your program," plus the model and pilot breakdown. NIL material was held back for the staff meeting. | Email "Chase Ames/ Edge3 Pilot" to travis.bush@utrgv.edu; page utrgvamesriskfit.netlify.app |
| July 15, 2026 | The staff demo built for UTRGV carried the Chase file: one year as a varsity starter in Texas 6A, 3,736 yards, 48 TD, 71 percent completions, 12-2; rhythm passer for a proven passing offense; low flight risk (in-state, 4.0 anchor, recruited-to-play fit); comp anchor "the Marburger arc," with Zappe and Mestemaker as the overlooked Texas passers who walked the same road. The file was labeled a comp-anchored EDGE3 staff evaluation. Sources pulled for it: Hudl film, MaxPreps, On3, PFF. | Session "Build Edge3 interactive demo for UTRGV coaching staff"; Desktop `edge3-utrgv-demo/index.html` |
| August 1 to 2, 2026 | Official offer letter from Cameron Herrera; Chase forwarded "It's official!" | Email "Official Offer Letter - 27 QB Chase Ames" |
| October 21, 2026 | Brian asked Cam about a revenue-share agreement for Chase's commitment. Cam: Coach Bush handles revenue share; UTRGV has not paid a high school recruit revenue share and has not raised it. | Email "Chase Ames" |
| In edge3-model | The pattern was generalized: `scripts/build_utrgv_fcs_comps.py` ("UTRGV FCS comp mapping, Chase Ames pattern, generalized") builds comps for every UTRGV player from rooms Coach Bush knows personally first (Texas State, UTSA, Houston), then regional G5, then the full cohort. The Garret Rangel comp card follows the same anchor ("your offense just made a Walter Payton Award finalist out of this room"). `docs/athletes/wallets/chase-ames/` is the public sample preview, structure only. | edge3-model repo |

Two things could not be retrieved from this environment: the two Netlify pages themselves (the domain does not resolve here, and their source is not in either repo, so they were deployed from the desktop), and the FBS/FCS media-guide mapping run. The only media-guide references in edge3-model are the FB-01b verification notes and the April 21 Positional Baselines scope, which proposed a one-time manual scrape of team media guides to fill OC and DC by year. `data/fcs/fcs_head_coaches_manual.csv` holds one row (Bush). The media-guide run is on the desktop or downloads, which this session cannot reach.

## Rules added

Three rules now sit in `RULES.md` beside this report and in the Edge3-demos `CLAUDE.md`, with a paste block for the edge3-model `CLAUDE.md` in `EDGE3_MODEL_CLAUDE_MD_ADDITION.md`:

1. Coach history, not program history. Baselines come from the coach's own career at every stop; a first-time head coach is read through his assistant stops; media guides are the source for OC, DC and position-coach assignments by year.
2. Map every position coach to the players he coached, ranked by NFL outcome, then production, then PFF grade, highest to lowest. LOW only when documented. Never train on LOW.
3. Every row carries its source; unverified stays labeled.

## Gaps and the next pass

- Full all-conference lists for Incarnate Word 2010 to 2017, Texas State 2004 to 2007 and 2021, Northwestern State, Angelo State, Tennessee State, Midwestern State 2022, and the official 2025 All-Southland roster beyond the names confirmed here.
- Recruiting ratings, sizes and hometowns for most listed players. These are the fields the archetype needs most and the public record covers least.
- Three employment holes: Aych 2008 to 2010, Regalado 2017 to 2019, Barela's 2014 Kansas high school.
- Bush's San Marcos HS assistant year could not be found in any source.
- 2026 in-season production under the new titles (Aych as play-caller, Henderson as pass game coordinator, Barela as run game coordinator, Jones on special teams) is not yet in the record.
- PFF grades for the UTRGV 2025 rows (the FCS pulls in Drive) and for the FCS stops generally; only the FBS tables were joined here.
- The FBS/FCS media-guide mapping run and the two Chase Ames Netlify pages, both on the desktop.

The per-coach dossiers follow. Each ends with its own confidence rating and gap list.

---
