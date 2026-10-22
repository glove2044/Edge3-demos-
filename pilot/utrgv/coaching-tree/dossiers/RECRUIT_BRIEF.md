# Recruiting profile brief (shared by all recruiting-profile agents)

Context: EDGE3 is mapping every player in the UTRGV coaching-tree dossiers to his recruiting rating, high school profile and combine or camp testing, so the position archetypes can be read in recruiting terms. You get a JSON list of players (one file). For each player, fill the fields below from the web.

## Fields to return per player (JSON object, one per player, in a single JSON array as your final message)

```
{
 "coach": "<as given>", "player": "<as given>", "stop": "<as given>",
 "class_year": 2016,                      // HS graduation / recruiting class year
 "stars_247": 3, "composite_247": 0.8444, // 247Sports Composite if available; else 247 own rating; say which in sources
 "stars_rivals": 3, "rivals_rating": 5.5, // if found
 "national_rank_247": 174, "position_rank_247": 12, "state_rank_247": 25,
 "hs_name": "Cypress Falls", "hs_city": "Houston", "hs_state": "TX",
 "origin": "HS | JUCO | transfer-down (from <school>) | walk-on | international",   // path into the stop's program
 "height_signing": "6-1", "weight_signing": 215,     // at signing / on the recruiting profile
 "hs_stats": "senior: 120 tkl, 8 sacks; junior: ...",  // MaxPreps / press, one line
 "hs_honors": "all-district 1st team; Texas 6A all-state HM",
 "combine": {"forty": 4.62, "shuttle": 4.21, "vertical": 34.5, "broad": "9-11", "bench": null, "source": "Nike Opening Houston 2015 / 247 profile / Rivals camp", "verified": true},
 "sources": ["https://247sports.com/...", "https://www.maxpreps.com/...", "..."],
 "confidence": "High | Medium | Low",
 "notes": "disagreements, ambiguity (same-name players), anything unverified"
}
```

## Rules

- Use WebSearch (works). WebFetch fails on most domains here (DNS), so take values from search-result excerpts of 247Sports, Rivals, On3, ESPN recruiting, MaxPreps, Hudl, school signing-day releases, and local press. Cite the URL for every value.
- Never invent a number. Use null for anything not found and say so in notes. Combine and camp numbers are often missing for older or lightly recruited players; null is the honest answer.
- Same-name risk is high (e.g., Dan Foster, Jordan Smith, Jalen Thompson, Tyler Williams, Josh Jones). Confirm identity with the college school and years in the "known"/"context" fields before attributing a profile. If you cannot confirm, return the candidate with confidence Low and explain.
- "known" fields were pre-filled from EDGE3's local 247/CFBD tables. If the status says "unverified name match; confirm", your first job is to confirm or reject that match.
- Players at the UTRGV 2025 stop are current or recent FCS players; their recruiting pages exist on 247/On3 and the UTRGV signing releases (goutrgv.com snippets).
- Pro-only rows (Bills 2015, Brahmas) still have HS recruiting profiles; fill what you can quickly, do not spend more than two searches on them.
- Budget: roughly 3 searches per player. Prioritize TOP rows over LOW rows, and rating + HS + height/weight over combine numbers. If the search budget runs out, return what you have and list the players you did not reach in a final "unreached" array.
- Return ONLY the JSON array (plus an "unreached" array if needed) as your final message. No prose outside JSON.
