-- EDGE3-xx: the coaching tree as league-wide reference (coach history, not program
-- history). Three tables, built from public sources only (school bios, conference
-- releases, 247/Rivals/MaxPreps, licensed PFF grades), never from a school's private
-- input, so RLS stays OFF and every tenant may read them (same reasoning as
-- 20260915000100_rls, "league-wide reference"). The loader writes them; the app reads.
--
-- Seeds: pilot/utrgv/coaching-tree/pilot/coaching_tree_{coaches,stops,players}.csv
-- (Edge3-demos, branch claude/utrgv-coaching-tree-history-hp4dlh). Column names match.

CREATE TABLE "CoachStaff" (
    "id"             TEXT NOT NULL,            -- coach_id slug, e.g. travis-bush
    "coachName"      TEXT NOT NULL,
    "program"        TEXT NOT NULL,            -- "UT Rio Grande Valley" (School.rosterTeam)
    "season"         INTEGER NOT NULL,         -- staff season this row describes
    "title"          TEXT NOT NULL,            -- utrgv_title
    "room"           TEXT,                     -- HC | QB | RB | WR | TE | OL | DL | EDGE | LB | S | CB
    "mentors"        TEXT,                     -- " | "-joined
    "archetypeRead"  TEXT,                     -- " | "-joined bullets; priors, never model output
    "hcArchetype"    TEXT,
    "confidence"     TEXT,
    "gaps"           TEXT,
    "source"         TEXT NOT NULL,
    "createdAt"      TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "CoachStaff_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "CoachStaff_program_season_idx" ON "CoachStaff"("program", "season");

CREATE TABLE "CoachStop" (
    "id"          TEXT NOT NULL,
    "coachId"     TEXT NOT NULL,
    "stopOrder"   INTEGER NOT NULL,
    "years"       TEXT NOT NULL,
    "school"      TEXT NOT NULL,
    "role"        TEXT NOT NULL,
    "workedUnder" TEXT,
    "sources"     TEXT NOT NULL,
    CONSTRAINT "CoachStop_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "CoachStop_coachId_stopOrder_key" ON "CoachStop"("coachId", "stopOrder");
ALTER TABLE "CoachStop" ADD CONSTRAINT "CoachStop_coachId_fkey" FOREIGN KEY ("coachId") REFERENCES "CoachStaff"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- One row per player a coach produced (TOP) or lost (LOW) at a stop, ranked within the
-- stop by NFL outcome, then production, then PFF (Rule 2), with the recruiting profile
-- (Rule 4). playerId links to Player when entity resolution finds him (UTRGV rows carry
-- cfbdPlayerId); historical rows at other schools usually will not resolve and that is fine.
CREATE TABLE "CoachTreePlayer" (
    "id"               TEXT NOT NULL,
    "coachId"          TEXT NOT NULL,
    "stop"             TEXT NOT NULL,
    "tier"             TEXT NOT NULL,          -- TOP | LOW
    "rank"             INTEGER NOT NULL,
    "playerName"       TEXT NOT NULL,
    "playerId"         TEXT,                   -- Player.id once resolved
    "cfbdPlayerId"     TEXT,
    "position"         TEXT,
    "years"            TEXT,
    "nflLevel"         INTEGER NOT NULL DEFAULT 0,   -- 3 drafted/roster/honors, 2 UDFA/camp/other pro, 0 none
    "honorLevel"       INTEGER NOT NULL DEFAULT 0,   -- 6 AA/POY … 1 stats only
    "pffBestGrade"     DOUBLE PRECISION,
    "pffSeason"        INTEGER,
    "pffSource"        TEXT,
    "recruitClass"     INTEGER,
    "stars247"         INTEGER,
    "composite247"     DOUBLE PRECISION,
    "starsRivals"      INTEGER,
    "nationalRank247"  INTEGER,
    "hsName"           TEXT,
    "hsCity"           TEXT,
    "hsState"          TEXT,
    "origin"           TEXT,                   -- HS | JUCO | transfer-down (from X) | walk-on | pro
    "heightSigning"    TEXT,
    "weightSigning"    INTEGER,
    "hsStats"          TEXT,
    "hsHonors"         TEXT,
    "forty"            DOUBLE PRECISION,
    "shuttle"          DOUBLE PRECISION,
    "vertical"         DOUBLE PRECISION,
    "broad"            TEXT,
    "combineSource"    TEXT,
    "recruitMatchStatus" TEXT,
    "recruitConfidence"  TEXT,
    "outcome"          TEXT NOT NULL,          -- the documented honor / what happened
    "sources"          TEXT NOT NULL,
    "recruitSources"   TEXT,
    "createdAt"        TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "CoachTreePlayer_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "CoachTreePlayer_coachId_stop_tier_rank_key" ON "CoachTreePlayer"("coachId", "stop", "tier", "rank");
CREATE INDEX "CoachTreePlayer_playerId_idx" ON "CoachTreePlayer"("playerId");
CREATE INDEX "CoachTreePlayer_cfbdPlayerId_idx" ON "CoachTreePlayer"("cfbdPlayerId");
ALTER TABLE "CoachTreePlayer" ADD CONSTRAINT "CoachTreePlayer_coachId_fkey" FOREIGN KEY ("coachId") REFERENCES "CoachStaff"("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "CoachTreePlayer" ADD CONSTRAINT "CoachTreePlayer_playerId_fkey" FOREIGN KEY ("playerId") REFERENCES "Player"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- Default privileges hand a new table to nobody (20260915000100); these are the
-- deliberate grants, mirroring PlayerComparable and PlayerFact exactly.
GRANT SELECT ON "CoachStaff", "CoachStop", "CoachTreePlayer" TO edge3_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON "CoachStaff", "CoachStop", "CoachTreePlayer" TO edge3_loader;
