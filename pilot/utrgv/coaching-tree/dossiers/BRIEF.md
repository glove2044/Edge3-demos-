# Coaching tree research brief (shared by all research agents)

Client context: EDGE3 is building a recruiting-intelligence pilot for UTRGV Football (FCS, Southland Conference; first season 2025; head coach Travis Bush, a first-time college head coach). EDGE3 maps each coach's "coaching tree": every stop in the coach's career, who they worked under, and the TOP-performing and LOW-performing players they coached at each stop. The output feeds a position "archetype" (what the coach's best players had in common) for Dennis, EDGE3's engineer, who will load it into the pilot.

## What to produce for EACH coach assigned to you

1. Career timeline, oldest to newest: year range, school, exact role, head coach and coordinator they worked under. Cite the source URL for each row. Primary sources: the coach's official UTRGV bio (goutrgv.com, may not resolve from this environment; use the search snippet or a cached copy), prior schools' staff bios, Wikipedia, texasfootball.com, 247Sports, Rivals, conference sites, local papers.
2. Tree: the mentors (head coaches and coordinators) at each stop, and the scheme or system associated with them if documented.
3. Players, per stop where the coach ran a position group (or, for a coordinator, the side of the ball):
   - TOP performers: players they coached who earned all-conference, All-American, conference player of the year, NFL draft or NFL roster, or school records. Include year(s) coached, position, honor, and source URL.
   - LOW performers: players who were highly rated or expected to produce under this coach but did not (transferred out, lost the job, dismissed, never started despite rating). Only include when a source documents it. Never invent, and never label a player "low" from your own judgment alone.
   - Target 3 to 6 TOP and 2 to 4 LOW per stop where data exists. For FCS, D2, JUCO and high school stops, data will be thin; say "thin" and give what exists (all-district, college signees, state honors).
4. Archetype read, 3 to 6 bullets: what the TOP performers have in common (size, recruiting rating, home state, HS vs JUCO vs transfer origin, athletic profile, scheme fit). Base it only on the players you listed. Note where the LOW performers broke the pattern.
5. Confidence: High, Medium, or Low for the timeline and for the player lists, with one sentence on why.

## Rules
- Every factual claim about a person or a school needs a URL. If you cannot find a source, write "not found" instead of guessing.
- Mark anything uncertain as "unverified". Sources disagree sometimes (titles, years). Report the disagreement rather than picking silently.
- Use WebSearch first (it works). WebFetch may fail on some domains (goutrgv.com does not resolve here); try Wikipedia, ESPN, school sites, news sites, 247Sports, sports-reference.com (cfb) when a fetch fails.
- Do not write code. Do not create files. Return your findings as the final message, in Markdown, using exactly the section headings below for each coach so the results can be merged.
- Keep each coach to roughly 400 to 900 words. Dense tables are good.

## Output template (repeat per coach)

### <Coach name> — <UTRGV title>
**Timeline**
| Years | School | Role | Worked under (HC / coordinator) | Source |

**Tree / mentors**
- ...

**Players by stop**
#### <Stop, years>
TOP:
| Player | Pos | Years | Honor / outcome | Source |
LOW:
| Player | Pos | Years | What happened | Source |

**Archetype read**
- ...

**Confidence**: Timeline <H/M/L> (why). Players <H/M/L> (why).

**Gaps**: what could not be found.
