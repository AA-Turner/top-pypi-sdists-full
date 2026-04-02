"""SQLite schema creation and database access."""

from __future__ import annotations

import asyncio
import logging
import sqlite3
import threading
import time

from .. import config

logger = logging.getLogger(__name__)

# Max retries and backoff for database-locked errors across processes.
# With 12 retries starting at 0.1s the total window is ~60s
# (0.1+0.2+0.4+...+204.8) matching busy_timeout=60000ms,
# plus random jitter (50%-150%) to avoid thundering-herd collisions.
_DB_RETRY_MAX = 12
_DB_RETRY_BACKOFF = 0.1  # seconds, doubles each attempt

# Singleton connection — avoids opening multiple connections per process
# which causes "database is locked" errors with WAL mode.
_conn: sqlite3.Connection | None = None


class _UnclosableConnection:
    """Wrapper that prevents closing the shared singleton connection.

    Existing code calls db.close() after each query. With a singleton
    connection this would break subsequent queries. This wrapper makes
    close() a no-op while proxying everything else to the real connection.

    Additionally, execute(), executemany(), executescript(), and commit()
    automatically retry on "database is locked" errors with exponential
    backoff to handle concurrent MCP server processes.
    """

    __slots__ = ("_real",)

    def __init__(self, conn: sqlite3.Connection) -> None:
        object.__setattr__(self, "_real", conn)

    def close(self) -> None:  # noqa: D102
        pass  # No-op: keep the singleton alive

    # -- Retry wrappers for write operations --

    def _retry(self, method_name: str, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003, ANN202
        import random

        real = object.__getattribute__(self, "_real")
        method = getattr(real, method_name)
        for attempt in range(_DB_RETRY_MAX):
            try:
                return method(*args, **kwargs)
            except sqlite3.OperationalError as exc:
                if "locked" not in str(exc).lower():
                    raise
                if attempt == _DB_RETRY_MAX - 1:
                    raise
                # Exponential backoff with jitter (50%-150%) to avoid thundering herd
                base_wait = _DB_RETRY_BACKOFF * (2 ** attempt)
                wait = base_wait * (0.5 + random.random())
                logger.warning("DB locked on %s, retry %d/%d after %.2fs", method_name, attempt + 1, _DB_RETRY_MAX, wait)
                time.sleep(wait)

    def execute(self, *args, **kwargs):  # noqa: ANN002, ANN003, ANN201
        return self._retry("execute", *args, **kwargs)

    def executemany(self, *args, **kwargs):  # noqa: ANN002, ANN003, ANN201
        return self._retry("executemany", *args, **kwargs)

    def executescript(self, *args, **kwargs):  # noqa: ANN002, ANN003, ANN201
        return self._retry("executescript", *args, **kwargs)

    def commit(self, *args, **kwargs):  # noqa: ANN002, ANN003, ANN201
        return self._retry("commit", *args, **kwargs)

    def __getattr__(self, name: str):  # noqa: ANN204
        return getattr(object.__getattribute__(self, "_real"), name)

    def __setattr__(self, name: str, value: object) -> None:
        setattr(object.__getattribute__(self, "_real"), name, value)


_SCHEMA_SQL = """
-- Core settings (voice signature, preferences, etc.)
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- Campaigns
CREATE TABLE IF NOT EXISTS campaigns (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    icp_json    TEXT,
    status      TEXT NOT NULL DEFAULT 'draft',
    mode        TEXT NOT NULL DEFAULT 'autopilot',
    config_json TEXT,
    created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- Contacts (prospects)
CREATE TABLE IF NOT EXISTS contacts (
    id            TEXT PRIMARY KEY,
    campaign_id   TEXT,
    name          TEXT,
    title         TEXT,
    company       TEXT,
    linkedin_url  TEXT,
    linkedin_id   TEXT,
    profile_json  TEXT,
    analysis_json TEXT,
    fit_score     REAL DEFAULT 0.0,
    status        TEXT NOT NULL DEFAULT 'pending',
    created_at    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at    INTEGER,
    source        TEXT DEFAULT 'search',
    source_detail TEXT DEFAULT '',
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Outreaches (one per contact per campaign)
CREATE TABLE IF NOT EXISTS outreaches (
    id              TEXT PRIMARY KEY,
    campaign_id     TEXT NOT NULL,
    contact_id      TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    next_action     TEXT,
    scheduled_at    INTEGER,
    followup_count  INTEGER NOT NULL DEFAULT 0,
    outcome_json    TEXT,
    invited_at      INTEGER,
    accepted_at     INTEGER,
    first_reply_at  INTEGER,
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);

-- Messages (conversation thread)
CREATE TABLE IF NOT EXISTS messages (
    id          TEXT PRIMARY KEY,
    outreach_id TEXT NOT NULL,
    role        TEXT NOT NULL,  -- 'sdr' or 'prospect'
    text        TEXT NOT NULL,
    sentiment   TEXT,
    read_at     INTEGER,  -- Unix timestamp when prospect read our message (NULL = unread/unknown)
    timestamp   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (outreach_id) REFERENCES outreaches(id)
);

-- Actions log (audit trail)
CREATE TABLE IF NOT EXISTS actions_log (
    id           TEXT PRIMARY KEY,
    outreach_id  TEXT,
    action_type  TEXT NOT NULL,
    result       TEXT,
    details_json TEXT,
    timestamp    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (outreach_id) REFERENCES outreaches(id)
);

-- Rate limits (per day)
CREATE TABLE IF NOT EXISTS rate_limits (
    id          TEXT PRIMARY KEY,
    date        TEXT NOT NULL UNIQUE,
    sent        INTEGER NOT NULL DEFAULT 0,
    accepted    INTEGER NOT NULL DEFAULT 0,
    daily_limit INTEGER NOT NULL DEFAULT 15,
    blocked     INTEGER NOT NULL DEFAULT 0,
    updated_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- Email rate limits (overflow channel — separate from LinkedIn limits)
CREATE TABLE IF NOT EXISTS email_rate_limits (
    id          TEXT PRIMARY KEY,
    date        TEXT NOT NULL UNIQUE,
    sent        INTEGER NOT NULL DEFAULT 0,
    updated_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- Usage tracking (free tier monthly counters)
CREATE TABLE IF NOT EXISTS usage (
    month              TEXT PRIMARY KEY,  -- 'YYYY-MM'
    invitations_sent   INTEGER NOT NULL DEFAULT 0,
    messages_sent      INTEGER NOT NULL DEFAULT 0,
    campaigns_created  INTEGER NOT NULL DEFAULT 0,
    icps_generated     INTEGER NOT NULL DEFAULT 0,
    engagements_sent   INTEGER NOT NULL DEFAULT 0,
    updated_at         INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- ICPs (persisted Ideal Customer Profiles)
CREATE TABLE IF NOT EXISTS icps (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    icp_json    TEXT NOT NULL,      -- full IcpResult serialized as JSON
    target_desc TEXT,               -- original target description
    source_url  TEXT,               -- company URL if provided
    status      TEXT NOT NULL DEFAULT 'active',
    confidence  REAL DEFAULT 0.5,   -- best ICP confidence score
    created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- ICP data sources (websites, text, KB)
CREATE TABLE IF NOT EXISTS icp_sources (
    id          TEXT PRIMARY KEY,
    icp_id      TEXT,
    source_type TEXT NOT NULL,      -- 'website', 'text', 'kb'
    uri         TEXT,
    title       TEXT,
    content_hash TEXT,
    chunk_count INTEGER DEFAULT 0,
    created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (icp_id) REFERENCES icps(id)
);

-- ICP chunks (for RAG, Phase 2+)
CREATE TABLE IF NOT EXISTS icp_chunks (
    id          TEXT PRIMARY KEY,
    source_id   TEXT NOT NULL,
    text        TEXT NOT NULL,
    ctx_text    TEXT,               -- chunk + surrounding context
    header_path TEXT DEFAULT '',
    position    INTEGER DEFAULT 0,
    embedding   BLOB,              -- numpy float32 array (Phase 3+)
    created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (source_id) REFERENCES icp_sources(id)
);

-- Engagements (post comments and reactions)
CREATE TABLE IF NOT EXISTS engagements (
    id            TEXT PRIMARY KEY,
    outreach_id   TEXT,
    action_type   TEXT NOT NULL,       -- 'comment' or 'react'
    post_id       TEXT NOT NULL,       -- LinkedIn post ID/URN
    post_text     TEXT,                -- Snapshot of the post text (for context)
    text          TEXT,                -- Comment text (null for reactions)
    reaction_type TEXT,                -- 'LIKE', 'CELEBRATE', etc. (null for comments)
    status        TEXT NOT NULL DEFAULT 'sent',  -- 'sent', 'pending_review', 'failed'
    reasoning     TEXT,                -- JSON: LLM reasoning for comment choice
    created_at    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (outreach_id) REFERENCES outreaches(id)
);

-- Scheduler jobs (Sprint 17: autonomous scheduling)
CREATE TABLE IF NOT EXISTS scheduler_jobs (
    id           TEXT PRIMARY KEY,
    campaign_id  TEXT,              -- NULL for account-level (non-campaign) jobs
    outreach_id  TEXT,
    job_type     TEXT NOT NULL,     -- 'invite', 'followup', 'engage', 'check_replies'
    status       TEXT NOT NULL DEFAULT 'pending',  -- 'pending', 'running', 'completed', 'failed'
    scheduled_at INTEGER NOT NULL,
    started_at   INTEGER,
    completed_at INTEGER,
    retry_count  INTEGER NOT NULL DEFAULT 0,
    error        TEXT,
    created_at   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (outreach_id) REFERENCES outreaches(id)
);

-- Experiments (PM hypothesis tracking)
CREATE TABLE IF NOT EXISTS experiments (
    id          TEXT PRIMARY KEY,
    snapshot    TEXT NOT NULL,
    result_json TEXT NOT NULL,
    campaign_ids TEXT,
    status      TEXT NOT NULL DEFAULT 'pending',
    created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- A/B Tests (controlled experiments on messaging variants and headlines)
CREATE TABLE IF NOT EXISTS ab_tests (
    id           TEXT PRIMARY KEY,
    campaign_id  TEXT NOT NULL,
    name         TEXT NOT NULL,          -- e.g., "Pain-first vs Question-first hook"
    hypothesis   TEXT,                   -- what we expect to learn
    variant_a    TEXT NOT NULL,          -- description of variant A (control)
    variant_b    TEXT NOT NULL,          -- description of variant B (treatment)
    test_type    TEXT NOT NULL DEFAULT 'message',  -- 'message' or 'headline'
    status       TEXT NOT NULL DEFAULT 'running',  -- running, completed, cancelled
    winner       TEXT,                   -- 'A', 'B', or 'inconclusive'
    result_json  TEXT,                   -- per-variant stats at completion
    created_at   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    completed_at INTEGER,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Inbound signals (connection requests, unsolicited DMs, post comments)
CREATE TABLE IF NOT EXISTS inbound_signals (
    id                 TEXT PRIMARY KEY,
    signal_type        TEXT NOT NULL,       -- 'invitation', 'message', 'comment'
    sender_name        TEXT,
    sender_id          TEXT,                -- LinkedIn provider_id
    sender_headline    TEXT,
    sender_company     TEXT,
    sender_url         TEXT,                -- LinkedIn profile URL
    content            TEXT,                -- invite message, DM text, or comment text
    post_id            TEXT,                -- only for comments (our post)
    profile_json       TEXT,                -- full profile if fetched
    intent             TEXT,                -- 'buying_signal', 'networking', 'job_seeking', 'spam', 'partnership', 'unknown'
    matched_icp_id     TEXT,
    confidence         REAL DEFAULT 0.0,
    recommended_action TEXT,                -- 'engage_immediately', 'ask_purpose', 'accept_and_monitor', 'ignore'
    reasoning          TEXT,
    status             TEXT DEFAULT 'new',  -- 'new', 'classified', 'accepted', 'ignored', 'declined', 'engaged', 'converted', 'dismissed'
    campaign_id        TEXT,
    created_at         INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    qualified_at       INTEGER,
    invitation_id      TEXT,                -- Unipile invitation ID for accept/decline
    actioned_at        INTEGER,             -- when accept/decline/DM was executed
    decline_reason     TEXT,                -- why declined (for auditing)
    message_id         TEXT,                -- LinkedIn message ID (for reactions)
    reaction_sent      INTEGER DEFAULT 0,   -- was a reaction sent?
    FOREIGN KEY (matched_icp_id) REFERENCES icps(id)
);

-- Published posts (for comment monitoring)
CREATE TABLE IF NOT EXISTS published_posts (
    id           TEXT PRIMARY KEY,
    post_id      TEXT NOT NULL,              -- LinkedIn post ID/URN
    text         TEXT,                       -- post content snapshot
    topic        TEXT,
    published_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    last_checked INTEGER,                    -- last time we checked for comments
    comment_count INTEGER DEFAULT 0
);

-- Proactive signals (buying intent from prospect behavior)
CREATE TABLE IF NOT EXISTS signals (
    id             TEXT PRIMARY KEY,
    signal_type    TEXT NOT NULL,             -- 'keyword_mention', 'prospect_post', 'job_change',
                                             -- 'competitor_mention', 'hiring_surge', 'funding_event',
                                             -- 'news_event', 'profile_view', 'post_engagement',
                                             -- 'commenter_match', 'company_change', 'promotion',
                                             -- 'headline_change', 'headline_intent'
    source         TEXT NOT NULL,             -- 'keyword_search', 'prospect_scan', 'profile_scan',
                                             -- 'job_search', 'news_search', 'comment_xref'
    prospect_id    TEXT,                      -- FK to contacts.id (NULL if new prospect)
    prospect_name  TEXT,
    prospect_title TEXT,
    linkedin_id    TEXT,                      -- LinkedIn provider_id (for dedup + linking)
    campaign_id    TEXT,                      -- FK to campaigns.id (if linked to campaign)

    -- Signal content
    content        TEXT,                      -- Post text, job description, news snippet
    post_id        TEXT,                      -- LinkedIn post ID (if post-related)
    metadata_json  TEXT,                      -- Flexible: {keywords_matched, company, old_title, new_title, etc.}

    -- Classification
    intent         TEXT,                      -- 'buying_signal', 'pain_point', 'competitor_eval',
                                             -- 'job_seeking', 'thought_leadership', 'unknown'
    confidence     REAL DEFAULT 0.0,          -- 0.0-1.0 (from classifier)
    signal_score   REAL DEFAULT 0.0,          -- 0.0-1.0 (composite weighted score)
    reasoning      TEXT,

    -- State
    status         TEXT DEFAULT 'new',        -- 'new', 'classified', 'actioned', 'dismissed', 'expired'
    action_taken   TEXT,                      -- 'campaign_created', 'outreach_triggered', 'engaged', NULL
    actioned_at    INTEGER,
    expires_at     INTEGER,                   -- Signal freshness expiry (auto-decay)

    detected_at    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    classified_at  INTEGER,

    FOREIGN KEY (prospect_id) REFERENCES contacts(id),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Signal watchlists (keyword monitoring configuration)
CREATE TABLE IF NOT EXISTS signal_watchlists (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,                -- e.g., "Competitor mentions", "Pain point keywords"
    watch_type  TEXT NOT NULL,                -- 'keyword', 'competitor', 'company', 'person'
    keywords    TEXT NOT NULL,                -- JSON array: ["cold outreach", "SDR automation"]
    campaign_id TEXT,                         -- Optional: link signals to specific campaign
    is_active   INTEGER DEFAULT 1,
    last_polled_at INTEGER,                   -- Last time this watchlist was polled
    created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);

-- Intent events (compound intent from stacked signals)
CREATE TABLE IF NOT EXISTS intent_events (
    id              TEXT PRIMARY KEY,
    linkedin_id     TEXT NOT NULL,
    company         TEXT,
    event_type      TEXT NOT NULL,             -- 'new_leader_building', 'active_evaluation',
                                               -- 'growth_mode', 'engaged_thought_leader',
                                               -- 'warm_inbound', 'multi_signal_hot'
    signal_ids      TEXT NOT NULL,             -- JSON array of contributing signal IDs
    signal_types    TEXT NOT NULL,             -- JSON array of contributing signal types
    composite_score REAL NOT NULL,
    action_taken    TEXT,                       -- 'outreach_created', 'priority_boosted', NULL
    detected_at     INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    expires_at      INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_intent_events_linkedin ON intent_events(linkedin_id);
CREATE INDEX IF NOT EXISTS idx_intent_events_type ON intent_events(event_type);
CREATE INDEX IF NOT EXISTS idx_intent_events_score ON intent_events(composite_score DESC);

-- Signal accounts (aggregated signal scores per prospect)
CREATE TABLE IF NOT EXISTS signal_accounts (
    linkedin_id     TEXT PRIMARY KEY,
    prospect_name   TEXT,
    company         TEXT,
    total_signals   INTEGER DEFAULT 0,
    composite_score REAL DEFAULT 0.0,
    top_signal_type TEXT,                     -- Most impactful signal type
    last_signal_at  INTEGER,
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- Strategy patterns (cross-campaign learned patterns)
CREATE TABLE IF NOT EXISTS strategy_patterns (
    id                      TEXT PRIMARY KEY,
    pattern_type            TEXT NOT NULL,
    pattern_key             TEXT NOT NULL,
    description             TEXT,
    evidence_json           TEXT NOT NULL,
    confidence              REAL DEFAULT 0.0,
    estimated_revenue_impact REAL DEFAULT 0.0,
    acceptance_rate         REAL,
    reply_rate              REAL,
    conversion_rate         REAL,
    sample_size             INTEGER DEFAULT 0,
    status                  TEXT DEFAULT 'active',
    discovered_at           INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    last_validated          INTEGER,
    created_at              INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);

-- Strategy actions (audit trail of autonomous actions)
CREATE TABLE IF NOT EXISTS strategy_actions (
    id              TEXT PRIMARY KEY,
    action_type     TEXT NOT NULL,
    campaign_id     TEXT,
    pattern_id      TEXT,
    details_json    TEXT NOT NULL,
    outcome_json    TEXT,
    status          TEXT DEFAULT 'applied',
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    measured_at     INTEGER,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
    FOREIGN KEY (pattern_id) REFERENCES strategy_patterns(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_experiments_created ON experiments(created_at);
CREATE INDEX IF NOT EXISTS idx_ab_tests_campaign ON ab_tests(campaign_id);
CREATE INDEX IF NOT EXISTS idx_ab_tests_status ON ab_tests(status);
CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_status ON scheduler_jobs(status, scheduled_at);
CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_campaign ON scheduler_jobs(campaign_id);
CREATE INDEX IF NOT EXISTS idx_contacts_campaign ON contacts(campaign_id);
CREATE INDEX IF NOT EXISTS idx_contacts_linkedin_id ON contacts(linkedin_id);
CREATE INDEX IF NOT EXISTS idx_outreaches_campaign ON outreaches(campaign_id);
CREATE INDEX IF NOT EXISTS idx_outreaches_campaign_status ON outreaches(campaign_id, status);
CREATE INDEX IF NOT EXISTS idx_outreaches_contact ON outreaches(contact_id);
CREATE INDEX IF NOT EXISTS idx_outreaches_status ON outreaches(status);
CREATE INDEX IF NOT EXISTS idx_messages_outreach ON messages(outreach_id);
CREATE INDEX IF NOT EXISTS idx_actions_log_outreach ON actions_log(outreach_id);
CREATE INDEX IF NOT EXISTS idx_rate_limits_date ON rate_limits(date);
CREATE INDEX IF NOT EXISTS idx_icps_status ON icps(status);
CREATE INDEX IF NOT EXISTS idx_icp_sources_icp ON icp_sources(icp_id);
CREATE INDEX IF NOT EXISTS idx_icp_chunks_source ON icp_chunks(source_id);
CREATE INDEX IF NOT EXISTS idx_engagements_outreach ON engagements(outreach_id);
CREATE INDEX IF NOT EXISTS idx_engagements_created ON engagements(created_at);
CREATE INDEX IF NOT EXISTS idx_engagements_post_id ON engagements(post_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_inbound_signals_status ON inbound_signals(status);
CREATE INDEX IF NOT EXISTS idx_inbound_signals_type ON inbound_signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_inbound_signals_sender ON inbound_signals(sender_id);
CREATE INDEX IF NOT EXISTS idx_published_posts_post ON published_posts(post_id);
CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(status);
CREATE INDEX IF NOT EXISTS idx_signals_type ON signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_signals_prospect ON signals(linkedin_id);
CREATE INDEX IF NOT EXISTS idx_signals_detected ON signals(detected_at);
CREATE INDEX IF NOT EXISTS idx_signals_score ON signals(signal_score DESC);
CREATE INDEX IF NOT EXISTS idx_signals_action ON signals(action_taken);
CREATE INDEX IF NOT EXISTS idx_signal_watchlists_active ON signal_watchlists(is_active);
CREATE INDEX IF NOT EXISTS idx_signal_watchlists_campaign ON signal_watchlists(campaign_id);

CREATE INDEX IF NOT EXISTS idx_strategy_patterns_type ON strategy_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_strategy_patterns_status ON strategy_patterns(status);
CREATE INDEX IF NOT EXISTS idx_strategy_patterns_revenue ON strategy_patterns(estimated_revenue_impact);
CREATE INDEX IF NOT EXISTS idx_strategy_actions_campaign ON strategy_actions(campaign_id);
CREATE INDEX IF NOT EXISTS idx_strategy_actions_type ON strategy_actions(action_type);
CREATE INDEX IF NOT EXISTS idx_strategy_actions_status ON strategy_actions(status);

-- Posts (external posts encountered during engagement/scanning)
CREATE TABLE IF NOT EXISTS posts (
    id                 TEXT PRIMARY KEY,
    post_id            TEXT NOT NULL UNIQUE,
    author_linkedin_id TEXT,
    author_name        TEXT,
    text               TEXT,
    topic              TEXT,
    analysis_json      TEXT,
    metrics_json       TEXT,
    source             TEXT DEFAULT 'search',
    first_seen_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    last_seen_at       INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_posts_post_id ON posts(post_id);
CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_linkedin_id);
CREATE INDEX IF NOT EXISTS idx_posts_topic ON posts(topic);
CREATE INDEX IF NOT EXISTS idx_posts_seen ON posts(last_seen_at DESC);

-- Post authors (accumulated author intelligence)
CREATE TABLE IF NOT EXISTS post_authors (
    linkedin_id     TEXT PRIMARY KEY,
    name            TEXT,
    headline        TEXT,
    company         TEXT,
    posts_seen      INTEGER DEFAULT 1,
    topics_json     TEXT DEFAULT '[]',
    first_seen_at   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    last_post_at    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    contact_id      TEXT,
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);
CREATE INDEX IF NOT EXISTS idx_post_authors_company ON post_authors(company);
CREATE INDEX IF NOT EXISTS idx_post_authors_last ON post_authors(last_post_at DESC);

-- Contacts unique constraint (one contact per campaign per LinkedIn profile)
CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_campaign_linkedin
    ON contacts(campaign_id, linkedin_id)
    WHERE linkedin_id IS NOT NULL AND linkedin_id != '';

-- Outreaches unique constraint (one active outreach per contact per campaign)
CREATE UNIQUE INDEX IF NOT EXISTS idx_outreaches_campaign_contact
    ON outreaches(campaign_id, contact_id);

-- Communication Strategist: daily action plans per prospect
CREATE TABLE IF NOT EXISTS prospect_daily_plans (
    id              TEXT PRIMARY KEY,
    outreach_id     TEXT NOT NULL,
    campaign_id     TEXT NOT NULL,
    plan_date       TEXT NOT NULL,
    planned_actions TEXT NOT NULL DEFAULT '[]',
    executed_actions TEXT NOT NULL DEFAULT '[]',
    feedback_score  REAL,
    plan_source     TEXT DEFAULT 'llm',
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (outreach_id) REFERENCES outreaches(id),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_daily_plans_outreach_date
    ON prospect_daily_plans(outreach_id, plan_date);
CREATE INDEX IF NOT EXISTS idx_daily_plans_campaign_date
    ON prospect_daily_plans(campaign_id, plan_date);
CREATE INDEX IF NOT EXISTS idx_daily_plans_date
    ON prospect_daily_plans(plan_date);

-- Company page posts tracked for engagement monitoring (Phase 2 intent expansion)
CREATE TABLE IF NOT EXISTS company_posts_tracked (
    id                   TEXT PRIMARY KEY,
    watchlist_id         TEXT NOT NULL,
    post_id              TEXT NOT NULL,
    post_text            TEXT,
    last_checked_at      INTEGER,
    known_commenters     TEXT DEFAULT '[]',
    known_reactors       TEXT DEFAULT '[]',
    created_at           INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (watchlist_id) REFERENCES signal_watchlists(id)
);
CREATE INDEX IF NOT EXISTS idx_cpt_watchlist ON company_posts_tracked(watchlist_id);
CREATE INDEX IF NOT EXISTS idx_cpt_post_id ON company_posts_tracked(post_id);
"""


def get_db() -> sqlite3.Connection:
    """Return a singleton SQLite connection with WAL mode enabled.

    Re-uses the same connection across the process lifetime to avoid
    "database is locked" errors from multiple open connections competing
    for the write lock.

    Raises RuntimeError if called directly from the asyncio event loop
    thread.  Use ``db.aio`` or ``await run_db(fn, ...)`` instead.
    """
    # Enforce: sync DB calls must not run on the event loop thread.
    # run_db() executes in a ThreadPoolExecutor so it bypasses this check.
    try:
        asyncio.get_running_loop()
        if threading.current_thread() is threading.main_thread():
            import traceback
            tb = "".join(traceback.format_stack())
            raise RuntimeError(
                "Sync DB call on event loop thread — use `from ..db import aio as db` "
                "and `await db.func(...)`, or `await run_db(func, ...)`.\n"
                f"Call stack:\n{tb}"
            )
    except RuntimeError as e:
        if "event loop" in str(e).lower() and "Sync DB" in str(e):
            raise  # re-raise our own error
        pass  # no running event loop — sync context is fine

    global _conn
    if _conn is not None:
        return _conn

    config.ensure_dirs()
    path = config.db_path()
    is_new = not path.exists()

    conn = sqlite3.connect(str(path), timeout=60, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=60000")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA synchronous=NORMAL")       # Safe for WAL; reduces fsync overhead
    conn.execute("PRAGMA wal_autocheckpoint=100")    # Checkpoint every ~400KB (default 1000 = ~4MB)

    if is_new:
        if config.config_path().exists():
            logger.warning(
                "Database was recreated but config already exists — "
                "previous data may have been lost. "
                "Check ~/.heylead/backups/ for recovery options."
            )
        logger.info(f"Creating new database at {path}")
        conn.executescript(_SCHEMA_SQL)
        conn.commit()
        _run_migrations(conn)
    else:
        _run_migrations(conn)

    # Compact WAL after migrations to prevent lock contention from large WAL files
    try:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    except sqlite3.OperationalError:
        pass  # Not critical — checkpoint will happen naturally

    _conn = _UnclosableConnection(conn)
    return _conn


def _run_migrations(conn: sqlite3.Connection) -> None:
    """Apply schema migrations to existing databases."""
    # Create a pre-migration backup if the database has meaningful data.
    try:
        row = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()
        if row and row[0] > 0:
            from .backup import create_backup, rotate_backups

            create_backup("pre-migration")
            rotate_backups()
    except Exception:
        pass  # Table may not exist yet on fresh DBs; skip backup

    # Sprint 2: Add followup_count to outreaches
    try:
        conn.execute("ALTER TABLE outreaches ADD COLUMN followup_count INTEGER NOT NULL DEFAULT 0")
        conn.commit()
        logger.info("Migration: added followup_count to outreaches")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Sprint 3: Add engagements table (for existing DBs created before Sprint 3)
    try:
        conn.execute("SELECT 1 FROM engagements LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS engagements (
                id            TEXT PRIMARY KEY,
                outreach_id   TEXT,
                action_type   TEXT NOT NULL,
                post_id       TEXT NOT NULL,
                post_text     TEXT,
                text          TEXT,
                reaction_type TEXT,
                status        TEXT NOT NULL DEFAULT 'sent',
                reasoning     TEXT,
                created_at    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                FOREIGN KEY (outreach_id) REFERENCES outreaches(id)
            );
            CREATE INDEX IF NOT EXISTS idx_engagements_outreach ON engagements(outreach_id);
            CREATE INDEX IF NOT EXISTS idx_engagements_created ON engagements(created_at);
        """)
        conn.commit()
        logger.info("Migration: added engagements table")

    # Sprint 3: Add engagements_sent to usage
    try:
        conn.execute("ALTER TABLE usage ADD COLUMN engagements_sent INTEGER NOT NULL DEFAULT 0")
        conn.commit()
        logger.info("Migration: added engagements_sent to usage")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Sprint 12: Add outcome_json to outreaches (close reason, notes, booking)
    try:
        conn.execute("ALTER TABLE outreaches ADD COLUMN outcome_json TEXT")
        conn.commit()
        logger.info("Migration: added outcome_json to outreaches")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Sprint 14: Add context_json to campaigns (offerings, case_studies, social_proofs, preferences)
    try:
        conn.execute("ALTER TABLE campaigns ADD COLUMN context_json TEXT")
        conn.commit()
        logger.info("Migration: added context_json to campaigns")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Sprint 16: Add memory_json to outreaches (structured follow-up decisions)
    try:
        conn.execute("ALTER TABLE outreaches ADD COLUMN memory_json TEXT")
        conn.commit()
        logger.info("Migration: added memory_json to outreaches")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Sprint 21: Add event timestamps to outreaches
    for col in ("invited_at", "accepted_at", "first_reply_at"):
        try:
            conn.execute(f"ALTER TABLE outreaches ADD COLUMN {col} INTEGER")
            conn.commit()
            logger.info(f"Migration: added {col} to outreaches")
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Backfill: estimate event timestamps from updated_at for pre-migration outreaches
    try:
        _backfilled = conn.execute("""
            UPDATE outreaches SET
                invited_at = CASE WHEN invited_at IS NULL AND status NOT IN ('pending', 'skipped')
                    THEN COALESCE(created_at, updated_at) ELSE invited_at END,
                accepted_at = CASE WHEN accepted_at IS NULL AND status IN (
                    'connected', 'messaged', 'replied', 'hot_lead',
                    'closed_happy', 'closed_unhappy', 'reverse_pitch', 'opted_out')
                    THEN updated_at ELSE accepted_at END,
                first_reply_at = CASE WHEN first_reply_at IS NULL AND status IN (
                    'replied', 'hot_lead', 'closed_happy', 'closed_unhappy',
                    'reverse_pitch', 'opted_out')
                    THEN updated_at ELSE first_reply_at END
            WHERE invited_at IS NULL OR accepted_at IS NULL OR first_reply_at IS NULL
        """).rowcount
        conn.commit()
        if _backfilled:
            logger.info("Migration: backfilled %d outreach event timestamps", _backfilled)
    except Exception as e:
        logger.debug("Timestamp backfill skipped: %s", e)

    # Sprint 17: Add scheduler_jobs table (for existing DBs created before Sprint 17)
    try:
        conn.execute("SELECT 1 FROM scheduler_jobs LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS scheduler_jobs (
                id           TEXT PRIMARY KEY,
                campaign_id  TEXT,
                outreach_id  TEXT,
                job_type     TEXT NOT NULL,
                status       TEXT NOT NULL DEFAULT 'pending',
                scheduled_at INTEGER NOT NULL,
                started_at   INTEGER,
                completed_at INTEGER,
                retry_count  INTEGER NOT NULL DEFAULT 0,
                error        TEXT,
                created_at   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
                FOREIGN KEY (outreach_id) REFERENCES outreaches(id)
            );
            CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_status ON scheduler_jobs(status, scheduled_at);
            CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_campaign ON scheduler_jobs(campaign_id);
        """)
        conn.commit()
        logger.info("Migration: added scheduler_jobs table")

    # Feature 1.4: Add read_at to messages (read receipt tracking)
    try:
        conn.execute("ALTER TABLE messages ADD COLUMN read_at INTEGER")
        conn.commit()
        logger.info("Migration: added read_at to messages")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Sprint 22: Add experiments table
    try:
        conn.execute("SELECT 1 FROM experiments LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS experiments (
                id TEXT PRIMARY KEY, snapshot TEXT NOT NULL, result_json TEXT NOT NULL,
                campaign_ids TEXT, status TEXT NOT NULL DEFAULT 'pending',
                created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_experiments_created ON experiments(created_at);
        """)
        conn.commit()
        logger.info("Migration: added experiments table")


    # Feature 3.2: Add variant column to outreaches (A/B testing)
    try:
        conn.execute("ALTER TABLE outreaches ADD COLUMN variant TEXT")
        conn.commit()
        logger.info("Migration: added variant to outreaches")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Feature 3.2: Add ab_tests table
    try:
        conn.execute("SELECT 1 FROM ab_tests LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS ab_tests (
                id           TEXT PRIMARY KEY,
                campaign_id  TEXT NOT NULL,
                name         TEXT NOT NULL,
                hypothesis   TEXT,
                variant_a    TEXT NOT NULL,
                variant_b    TEXT NOT NULL,
                status       TEXT NOT NULL DEFAULT 'running',
                winner       TEXT,
                result_json  TEXT,
                created_at   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                completed_at INTEGER,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );
            CREATE INDEX IF NOT EXISTS idx_ab_tests_campaign ON ab_tests(campaign_id);
            CREATE INDEX IF NOT EXISTS idx_ab_tests_status ON ab_tests(status);
        """)
        conn.commit()
        logger.info("Migration: added ab_tests table")


    # Feature 3.5: Add channel column to outreaches (linkedin/email)
    try:
        conn.execute("ALTER TABLE outreaches ADD COLUMN channel TEXT DEFAULT 'linkedin'")
        conn.commit()
        logger.info("Migration: added channel to outreaches")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Feature 3.5: Add channel column to messages
    try:
        conn.execute("ALTER TABLE messages ADD COLUMN channel TEXT DEFAULT 'linkedin'")
        conn.commit()
        logger.info("Migration: added channel to messages")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Feature 4.1: Add source column to contacts (search/import/discovery)
    try:
        conn.execute("ALTER TABLE contacts ADD COLUMN source TEXT DEFAULT 'search'")
        conn.commit()
        logger.info("Migration: added source to contacts")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Feature 4.4: CRM mappings table for HubSpot integration
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crm_mappings (
            id              TEXT PRIMARY KEY,
            contact_id      TEXT NOT NULL,
            crm_type        TEXT NOT NULL DEFAULT 'hubspot',
            crm_contact_id  TEXT,
            crm_deal_id     TEXT,
            synced_at       INTEGER,
            created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
            FOREIGN KEY (contact_id) REFERENCES contacts(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_crm_mappings_contact ON crm_mappings(contact_id)")
    conn.commit()

    # Inbound pipeline: inbound_signals table
    try:
        conn.execute("SELECT 1 FROM inbound_signals LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS inbound_signals (
                id                 TEXT PRIMARY KEY,
                signal_type        TEXT NOT NULL,
                sender_name        TEXT,
                sender_id          TEXT,
                sender_headline    TEXT,
                sender_company     TEXT,
                sender_url         TEXT,
                content            TEXT,
                post_id            TEXT,
                profile_json       TEXT,
                intent             TEXT,
                matched_icp_id     TEXT,
                confidence         REAL DEFAULT 0.0,
                recommended_action TEXT,
                reasoning          TEXT,
                status             TEXT DEFAULT 'new',
                campaign_id        TEXT,
                created_at         INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                qualified_at       INTEGER,
                FOREIGN KEY (matched_icp_id) REFERENCES icps(id)
            );
            CREATE INDEX IF NOT EXISTS idx_inbound_signals_status ON inbound_signals(status);
            CREATE INDEX IF NOT EXISTS idx_inbound_signals_type ON inbound_signals(signal_type);
            CREATE INDEX IF NOT EXISTS idx_inbound_signals_sender ON inbound_signals(sender_id);
        """)
        conn.commit()
        logger.info("Migration: added inbound_signals table")

    # Inbound pipeline: published_posts table
    try:
        conn.execute("SELECT 1 FROM published_posts LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS published_posts (
                id           TEXT PRIMARY KEY,
                post_id      TEXT NOT NULL,
                text         TEXT,
                topic        TEXT,
                published_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                last_checked INTEGER,
                comment_count INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_published_posts_post ON published_posts(post_id);
        """)
        conn.commit()
        logger.info("Migration: added published_posts table")

    # Signal-based selling: signals table (v1.0)
    try:
        conn.execute("SELECT 1 FROM signals LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS signals (
                id             TEXT PRIMARY KEY,
                signal_type    TEXT NOT NULL,
                source         TEXT NOT NULL,
                prospect_id    TEXT,
                prospect_name  TEXT,
                prospect_title TEXT,
                linkedin_id    TEXT,
                campaign_id    TEXT,
                content        TEXT,
                post_id        TEXT,
                metadata_json  TEXT,
                intent         TEXT,
                confidence     REAL DEFAULT 0.0,
                signal_score   REAL DEFAULT 0.0,
                reasoning      TEXT,
                status         TEXT DEFAULT 'new',
                action_taken   TEXT,
                actioned_at    INTEGER,
                expires_at     INTEGER,
                detected_at    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                classified_at  INTEGER,
                FOREIGN KEY (prospect_id) REFERENCES contacts(id),
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );
            CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(status);
            CREATE INDEX IF NOT EXISTS idx_signals_type ON signals(signal_type);
            CREATE INDEX IF NOT EXISTS idx_signals_prospect ON signals(linkedin_id);
            CREATE INDEX IF NOT EXISTS idx_signals_detected ON signals(detected_at);
            CREATE INDEX IF NOT EXISTS idx_signals_score ON signals(signal_score DESC);
            CREATE INDEX IF NOT EXISTS idx_signals_action ON signals(action_taken);
        """)
        conn.commit()
        logger.info("Migration: added signals table")

    # Signal-based selling: signal_watchlists table (v1.0)
    try:
        conn.execute("SELECT 1 FROM signal_watchlists LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS signal_watchlists (
                id          TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                watch_type  TEXT NOT NULL,
                keywords    TEXT NOT NULL,
                campaign_id TEXT,
                is_active   INTEGER DEFAULT 1,
                last_polled_at INTEGER,
                created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );
            CREATE INDEX IF NOT EXISTS idx_signal_watchlists_active ON signal_watchlists(is_active);
            CREATE INDEX IF NOT EXISTS idx_signal_watchlists_campaign ON signal_watchlists(campaign_id);
        """)
        conn.commit()
        logger.info("Migration: added signal_watchlists table")

    # Signal-based selling: signal_accounts table (v1.0)
    try:
        conn.execute("SELECT 1 FROM signal_accounts LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS signal_accounts (
                linkedin_id     TEXT PRIMARY KEY,
                prospect_name   TEXT,
                company         TEXT,
                total_signals   INTEGER DEFAULT 0,
                composite_score REAL DEFAULT 0.0,
                top_signal_type TEXT,
                last_signal_at  INTEGER,
                updated_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
        """)
        conn.commit()
        logger.info("Migration: added signal_accounts table")

    # Signal-based selling: last_scanned_at on contacts (v1.0)
    try:
        conn.execute("ALTER TABLE contacts ADD COLUMN last_scanned_at INTEGER")
        conn.commit()
        logger.info("Migration: added last_scanned_at to contacts")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Signal activation: signal_id on outreaches (v1.1)
    try:
        conn.execute("ALTER TABLE outreaches ADD COLUMN signal_id TEXT")
        conn.commit()
        logger.info("Migration: added signal_id to outreaches")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Strategy engine: estimated_revenue on contacts
    try:
        conn.execute("ALTER TABLE contacts ADD COLUMN estimated_revenue REAL DEFAULT 0.0")
        conn.commit()
        logger.info("Migration: added estimated_revenue to contacts")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Strategy engine: strategy_json on outreaches
    try:
        conn.execute("ALTER TABLE outreaches ADD COLUMN strategy_json TEXT")
        conn.commit()
        logger.info("Migration: added strategy_json to outreaches")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Strategy engine: spawned_by on campaigns
    try:
        conn.execute("ALTER TABLE campaigns ADD COLUMN spawned_by TEXT")
        conn.commit()
        logger.info("Migration: added spawned_by to campaigns")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Strategy engine: strategy_patterns table
    try:
        conn.execute("SELECT 1 FROM strategy_patterns LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS strategy_patterns (
                id                      TEXT PRIMARY KEY,
                pattern_type            TEXT NOT NULL,
                pattern_key             TEXT NOT NULL,
                description             TEXT,
                evidence_json           TEXT NOT NULL,
                confidence              REAL DEFAULT 0.0,
                estimated_revenue_impact REAL DEFAULT 0.0,
                acceptance_rate         REAL,
                reply_rate              REAL,
                conversion_rate         REAL,
                sample_size             INTEGER DEFAULT 0,
                status                  TEXT DEFAULT 'active',
                discovered_at           INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                last_validated          INTEGER,
                created_at              INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_strategy_patterns_type ON strategy_patterns(pattern_type);
            CREATE INDEX IF NOT EXISTS idx_strategy_patterns_status ON strategy_patterns(status);
            CREATE INDEX IF NOT EXISTS idx_strategy_patterns_revenue ON strategy_patterns(estimated_revenue_impact);
        """)
        conn.commit()
        logger.info("Migration: added strategy_patterns table")

    # Strategy engine: strategy_actions table
    try:
        conn.execute("SELECT 1 FROM strategy_actions LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS strategy_actions (
                id              TEXT PRIMARY KEY,
                action_type     TEXT NOT NULL,
                campaign_id     TEXT,
                pattern_id      TEXT,
                details_json    TEXT NOT NULL,
                outcome_json    TEXT,
                status          TEXT DEFAULT 'applied',
                created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                measured_at     INTEGER,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
                FOREIGN KEY (pattern_id) REFERENCES strategy_patterns(id)
            );
            CREATE INDEX IF NOT EXISTS idx_strategy_actions_campaign ON strategy_actions(campaign_id);
            CREATE INDEX IF NOT EXISTS idx_strategy_actions_type ON strategy_actions(action_type);
            CREATE INDEX IF NOT EXISTS idx_strategy_actions_status ON strategy_actions(status);
        """)
        conn.commit()
        logger.info("Migration: added strategy_actions table")


    # Tracking fix: add outreach_id to inbound_signals for message tracking
    try:
        conn.execute("ALTER TABLE inbound_signals ADD COLUMN outreach_id TEXT")
        conn.commit()
        logger.info("Migration: added outreach_id to inbound_signals")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Tracking fix: invite attempt tracking on outreaches
    for col, ctype in [("invite_attempts", "INTEGER NOT NULL DEFAULT 0"),
                        ("last_attempt_error", "TEXT")]:
        try:
            conn.execute(f"ALTER TABLE outreaches ADD COLUMN {col} {ctype}")
            conn.commit()
            logger.info("Migration: added %s to outreaches", col)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Tracking fix: campaign_id on engagements for manual engagement linking
    try:
        conn.execute("ALTER TABLE engagements ADD COLUMN campaign_id TEXT")
        conn.commit()
        logger.info("Migration: added campaign_id to engagements")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Compound intent events table (Week 10)
    try:
        conn.execute("SELECT 1 FROM intent_events LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS intent_events (
                id              TEXT PRIMARY KEY,
                linkedin_id     TEXT NOT NULL,
                company         TEXT,
                event_type      TEXT NOT NULL,
                signal_ids      TEXT NOT NULL,
                signal_types    TEXT NOT NULL,
                composite_score REAL NOT NULL,
                action_taken    TEXT,
                detected_at     INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                expires_at      INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_intent_events_linkedin ON intent_events(linkedin_id);
            CREATE INDEX IF NOT EXISTS idx_intent_events_type ON intent_events(event_type);
            CREATE INDEX IF NOT EXISTS idx_intent_events_score ON intent_events(composite_score DESC);
        """)
        conn.commit()
        logger.info("Migration: added intent_events table")


    # Voice memo support: format column on messages (voice memo sprint)
    try:
        conn.execute("ALTER TABLE messages ADD COLUMN format TEXT DEFAULT 'text'")
        conn.commit()
        logger.info("Migration: added format column to messages")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Fix: add updated_at to contacts (was missing from original schema)
    try:
        conn.execute("ALTER TABLE contacts ADD COLUMN updated_at INTEGER")
        conn.commit()
        logger.info("Migration: added updated_at to contacts")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Fix: convert empty-string campaign_id to NULL in scheduler_jobs
    # (global jobs used "" which violated FK constraint)
    try:
        updated = conn.execute(
            "UPDATE scheduler_jobs SET campaign_id = NULL WHERE campaign_id = ''"
        ).rowcount
        if updated:
            conn.commit()
            logger.info("Migration: converted %d scheduler_jobs campaign_id '' → NULL", updated)
    except sqlite3.OperationalError:
        pass

    # Partner follow-up tracking table
    try:
        conn.execute("SELECT 1 FROM partner_followups LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS partner_followups (
                id              TEXT PRIMARY KEY,
                name            TEXT NOT NULL,
                company         TEXT DEFAULT '',
                email           TEXT DEFAULT '',
                context         TEXT DEFAULT '',
                status          TEXT DEFAULT 'active',
                followup_count  INTEGER DEFAULT 0,
                next_followup   INTEGER,
                last_contacted  INTEGER,
                notes           TEXT DEFAULT '[]',
                created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                updated_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_partner_followups_status ON partner_followups(status);
            CREATE INDEX IF NOT EXISTS idx_partner_followups_next ON partner_followups(next_followup);
        """)
        conn.commit()
        logger.info("Migration: added partner_followups table")

    # Fix: make scheduler_jobs.campaign_id nullable for account-level jobs
    # Old migration created it as NOT NULL; recreate table with correct schema
    try:
        col_info = conn.execute("PRAGMA table_info(scheduler_jobs)").fetchall()
        for col in col_info:
            if col[1] == "campaign_id" and col[3] == 1:  # notnull=1
                conn.executescript("""
                    CREATE TABLE scheduler_jobs_new (
                        id           TEXT PRIMARY KEY,
                        campaign_id  TEXT,
                        outreach_id  TEXT,
                        job_type     TEXT NOT NULL,
                        status       TEXT NOT NULL DEFAULT 'pending',
                        scheduled_at INTEGER NOT NULL,
                        started_at   INTEGER,
                        completed_at INTEGER,
                        retry_count  INTEGER NOT NULL DEFAULT 0,
                        error        TEXT,
                        created_at   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                        FOREIGN KEY (campaign_id) REFERENCES campaigns(id),
                        FOREIGN KEY (outreach_id) REFERENCES outreaches(id)
                    );
                    INSERT INTO scheduler_jobs_new SELECT * FROM scheduler_jobs;
                    DROP TABLE scheduler_jobs;
                    ALTER TABLE scheduler_jobs_new RENAME TO scheduler_jobs;
                    CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_status ON scheduler_jobs(status, scheduled_at);
                    CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_campaign ON scheduler_jobs(campaign_id);
                """)
                conn.commit()
                logger.info("Migration: made scheduler_jobs.campaign_id nullable")
                break
    except sqlite3.OperationalError:
        pass

    # Profile change history: track all LinkedIn profile edits with restore
    try:
        conn.execute("SELECT 1 FROM profile_changes LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS profile_changes (
                id          TEXT PRIMARY KEY,
                field       TEXT NOT NULL,
                old_value   TEXT,
                new_value   TEXT NOT NULL,
                source      TEXT DEFAULT 'manual',
                status      TEXT DEFAULT 'applied',
                created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_profile_changes_field ON profile_changes(field);
            CREATE INDEX IF NOT EXISTS idx_profile_changes_created ON profile_changes(created_at DESC);
        """)
        conn.commit()
        logger.info("Migration: added profile_changes table")

    # Headline A/B testing: add test_type column to ab_tests
    try:
        conn.execute("SELECT test_type FROM ab_tests LIMIT 0")
    except sqlite3.OperationalError:
        conn.execute("ALTER TABLE ab_tests ADD COLUMN test_type TEXT NOT NULL DEFAULT 'message'")
        conn.commit()
        logger.info("Migration: added test_type column to ab_tests")

    # Observability: add duration_ms to scheduler_jobs for execution time tracking
    try:
        conn.execute("SELECT duration_ms FROM scheduler_jobs LIMIT 0")
    except sqlite3.OperationalError:
        conn.execute("ALTER TABLE scheduler_jobs ADD COLUMN duration_ms INTEGER")
        conn.commit()
        logger.info("Migration: added duration_ms column to scheduler_jobs")

    # Observability: scheduler_events table for structured event logging
    try:
        conn.execute("SELECT 1 FROM scheduler_events LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS scheduler_events (
                id          TEXT PRIMARY KEY,
                event_type  TEXT NOT NULL,
                campaign_id TEXT,
                outreach_id TEXT,
                job_id      TEXT,
                context     TEXT DEFAULT '{}',
                duration_ms INTEGER,
                created_at  INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_sched_evt_type ON scheduler_events(event_type);
            CREATE INDEX IF NOT EXISTS idx_sched_evt_time ON scheduler_events(created_at);
        """)
        conn.commit()
        logger.info("Migration: added scheduler_events table")

    # Engagement dedup: add account_id to track which LinkedIn account made each engagement
    try:
        conn.execute("SELECT account_id FROM engagements LIMIT 0")
    except sqlite3.OperationalError:
        conn.execute("ALTER TABLE engagements ADD COLUMN account_id TEXT")
        # Backfill existing rows with current account_id
        try:
            from ..linkedin import get_account_id
            aid = get_account_id() or ""
            if aid:
                conn.execute(
                    "UPDATE engagements SET account_id = ? WHERE account_id IS NULL",
                    (aid,),
                )
        except Exception:
            pass  # May fail during first init when no account is connected yet
        conn.commit()
        logger.info("Migration: added account_id to engagements")

    # Engagement dedup: index on post_id for fast global dedup queries
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_engagements_post_id ON engagements(post_id)"
    )

    # Engagement dedup: unique constraint — one engagement per post per account
    # Uses partial index to skip rows with NULL/empty account_id or post_id
    try:
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_engagements_post_account
            ON engagements(post_id, account_id)
            WHERE account_id IS NOT NULL AND account_id != '' AND post_id != ''
        """)
        conn.commit()
    except sqlite3.OperationalError:
        # May fail if duplicates already exist — clean them up first
        conn.execute("""
            DELETE FROM engagements WHERE id IN (
                SELECT id FROM (
                    SELECT id, ROW_NUMBER() OVER (
                        PARTITION BY post_id, account_id ORDER BY created_at ASC
                    ) as rn
                    FROM engagements
                    WHERE account_id IS NOT NULL AND account_id != '' AND post_id != ''
                ) WHERE rn > 1
            )
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_engagements_post_account
            ON engagements(post_id, account_id)
            WHERE account_id IS NOT NULL AND account_id != '' AND post_id != ''
        """)
        conn.commit()
        logger.info("Migration: cleaned duplicate engagements and added unique index")


    # Inbound pipeline: add dm_attempts for chat resolution retry tracking
    try:
        conn.execute("ALTER TABLE inbound_signals ADD COLUMN dm_attempts INTEGER DEFAULT 0")
        conn.commit()
        logger.info("Migration: added dm_attempts to inbound_signals")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # ── Post Intelligence: contacts unique constraint ──
    try:
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_campaign_linkedin
            ON contacts(campaign_id, linkedin_id)
            WHERE linkedin_id IS NOT NULL AND linkedin_id != ''
        """)
        conn.commit()
    except sqlite3.OperationalError:
        # Duplicates exist — clean up first (keep oldest per campaign+linkedin_id)
        conn.execute("""
            DELETE FROM contacts WHERE id IN (
                SELECT id FROM (
                    SELECT id, ROW_NUMBER() OVER (
                        PARTITION BY campaign_id, linkedin_id ORDER BY created_at ASC
                    ) as rn
                    FROM contacts
                    WHERE linkedin_id IS NOT NULL AND linkedin_id != ''
                ) WHERE rn > 1
            )
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_campaign_linkedin
            ON contacts(campaign_id, linkedin_id)
            WHERE linkedin_id IS NOT NULL AND linkedin_id != ''
        """)
        conn.commit()
        logger.info("Migration: cleaned duplicate contacts and added unique index")

    # ── Post Intelligence: posts table ──
    try:
        conn.execute("SELECT 1 FROM posts LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS posts (
                id                 TEXT PRIMARY KEY,
                post_id            TEXT NOT NULL UNIQUE,
                author_linkedin_id TEXT,
                author_name        TEXT,
                text               TEXT,
                topic              TEXT,
                analysis_json      TEXT,
                metrics_json       TEXT,
                source             TEXT DEFAULT 'search',
                first_seen_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                last_seen_at       INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE UNIQUE INDEX IF NOT EXISTS idx_posts_post_id ON posts(post_id);
            CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_linkedin_id);
            CREATE INDEX IF NOT EXISTS idx_posts_topic ON posts(topic);
            CREATE INDEX IF NOT EXISTS idx_posts_seen ON posts(last_seen_at DESC);
        """)
        conn.commit()
        logger.info("Migration: added posts table")

    # ── Post Intelligence: post_authors table ──
    try:
        conn.execute("SELECT 1 FROM post_authors LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS post_authors (
                linkedin_id     TEXT PRIMARY KEY,
                name            TEXT,
                headline        TEXT,
                company         TEXT,
                posts_seen      INTEGER DEFAULT 1,
                topics_json     TEXT DEFAULT '[]',
                first_seen_at   INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                last_post_at    INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                contact_id      TEXT,
                FOREIGN KEY (contact_id) REFERENCES contacts(id)
            );
            CREATE INDEX IF NOT EXISTS idx_post_authors_company ON post_authors(company);
            CREATE INDEX IF NOT EXISTS idx_post_authors_last ON post_authors(last_post_at DESC);
        """)
        conn.commit()
        logger.info("Migration: added post_authors table")


    # Global contact base: global_contacts table (master record per person)
    try:
        conn.execute("SELECT 1 FROM global_contacts LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS global_contacts (
                id                TEXT PRIMARY KEY,
                linkedin_id       TEXT,
                linkedin_url      TEXT,
                name              TEXT NOT NULL,
                title             TEXT DEFAULT '',
                company           TEXT DEFAULT '',
                email             TEXT DEFAULT '',
                location          TEXT DEFAULT '',
                profile_json      TEXT,
                analysis_json     TEXT,
                fit_score         REAL DEFAULT 0.0,
                estimated_revenue REAL DEFAULT 0.0,
                lifecycle_stage   TEXT DEFAULT 'prospect',
                tags_json         TEXT DEFAULT '[]',
                notes_json        TEXT DEFAULT '[]',
                source            TEXT DEFAULT 'search',
                source_detail     TEXT DEFAULT '',
                first_campaign_id TEXT,
                total_campaigns   INTEGER DEFAULT 0,
                first_contacted_at INTEGER,
                last_interaction_at INTEGER,
                created_at        INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                updated_at        INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE UNIQUE INDEX IF NOT EXISTS idx_global_contacts_linkedin
                ON global_contacts(linkedin_id)
                WHERE linkedin_id IS NOT NULL AND linkedin_id != '';
            CREATE INDEX IF NOT EXISTS idx_global_contacts_name ON global_contacts(name);
            CREATE INDEX IF NOT EXISTS idx_global_contacts_company ON global_contacts(company);
            CREATE INDEX IF NOT EXISTS idx_global_contacts_lifecycle ON global_contacts(lifecycle_stage);
            CREATE INDEX IF NOT EXISTS idx_global_contacts_score ON global_contacts(fit_score DESC);
            CREATE INDEX IF NOT EXISTS idx_global_contacts_updated ON global_contacts(updated_at DESC);
        """)
        conn.commit()
        logger.info("Migration: added global_contacts table")

    # Global contact base: FK column on contacts
    try:
        conn.execute("ALTER TABLE contacts ADD COLUMN global_contact_id TEXT")
        conn.commit()
        logger.info("Migration: added global_contact_id to contacts")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_contacts_global ON contacts(global_contact_id)"
    )
    conn.commit()

    # Communication Strategist: prospect_daily_plans table
    try:
        conn.execute("SELECT 1 FROM prospect_daily_plans LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS prospect_daily_plans (
                id              TEXT PRIMARY KEY,
                outreach_id     TEXT NOT NULL,
                campaign_id     TEXT NOT NULL,
                plan_date       TEXT NOT NULL,
                planned_actions TEXT NOT NULL DEFAULT '[]',
                executed_actions TEXT NOT NULL DEFAULT '[]',
                feedback_score  REAL,
                plan_source     TEXT DEFAULT 'llm',
                created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                updated_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                FOREIGN KEY (outreach_id) REFERENCES outreaches(id),
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );
            CREATE UNIQUE INDEX IF NOT EXISTS idx_daily_plans_outreach_date
                ON prospect_daily_plans(outreach_id, plan_date);
            CREATE INDEX IF NOT EXISTS idx_daily_plans_campaign_date
                ON prospect_daily_plans(campaign_id, plan_date);
            CREATE INDEX IF NOT EXISTS idx_daily_plans_date
                ON prospect_daily_plans(plan_date);
        """)
        conn.commit()
        logger.info("Migration: added prospect_daily_plans table")

    # Network Intelligence: add columns to global_contacts
    for col_name, col_def in [
        ("contact_info_json", "TEXT DEFAULT '{}'"),
        ("network_degree", "INTEGER DEFAULT NULL"),
        ("enriched_via", "TEXT DEFAULT ''"),
    ]:
        try:
            conn.execute(f"ALTER TABLE global_contacts ADD COLUMN {col_name} {col_def}")
            conn.commit()
            logger.info("Migration: added %s to global_contacts", col_name)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Convert permanent skip_engagement to 1h time-limited cooldown.
    # Permanent blocks are no longer set (replaced with JSON cooldowns in v0.9.42).
    try:
        import json as _json
        _cooldown = _json.dumps({"skip_engagement_until": int(time.time()) + 3600})
        cursor = conn.execute(
            "UPDATE outreaches SET next_action = ? WHERE next_action = 'skip_engagement'",
            (_cooldown,),
        )
        conn.commit()  # Always commit to avoid dangling write transaction
        if cursor.rowcount > 0:
            logger.info(
                "Migration: converted %d permanent skip_engagement to 1h cooldown",
                cursor.rowcount,
            )
    except Exception:
        pass  # Safe to skip — new code already writes JSON cooldowns

    # Prospect source tracking: add source_detail column
    for _tbl in ("contacts", "global_contacts"):
        try:
            conn.execute(f"ALTER TABLE {_tbl} ADD COLUMN source_detail TEXT DEFAULT ''")
            conn.commit()
            logger.info("Migration: added source_detail to %s", _tbl)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Action tracking: add campaign_id to actions_log for time-windowed campaign queries
    try:
        conn.execute("ALTER TABLE actions_log ADD COLUMN campaign_id TEXT")
        conn.commit()
        logger.info("Migration: added campaign_id to actions_log")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Action tracking: backfill actions_log.campaign_id from outreaches
    try:
        updated = conn.execute("""
            UPDATE actions_log SET campaign_id = (
                SELECT o.campaign_id FROM outreaches o WHERE o.id = actions_log.outreach_id
            ) WHERE campaign_id IS NULL AND outreach_id IS NOT NULL
        """).rowcount
        if updated:
            conn.commit()
            logger.info("Migration: backfilled campaign_id on %d actions_log rows", updated)
    except sqlite3.OperationalError:
        pass

    # Action tracking: indexes on actions_log for time-windowed reporting
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_actions_log_timestamp ON actions_log(timestamp)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_actions_log_type_time ON actions_log(action_type, timestamp)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_actions_log_campaign_time ON actions_log(campaign_id, timestamp)"
    )
    conn.commit()

    # Action verification: add verified_at and verified_status to outreaches
    for col, ctype in [("verified_at", "INTEGER"), ("verified_status", "TEXT")]:
        try:
            conn.execute(f"ALTER TABLE outreaches ADD COLUMN {col} {ctype}")
            conn.commit()
            logger.info("Migration: added %s to outreaches", col)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Engagement verification: add verified_at, verified_status, external_id to engagements
    for col, ctype in [
        ("verified_at", "INTEGER"),
        ("verified_status", "TEXT"),
        ("external_id", "TEXT"),
    ]:
        try:
            conn.execute(f"ALTER TABLE engagements ADD COLUMN {col} {ctype}")
            conn.commit()
            logger.info("Migration: added %s to engagements", col)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Local connections cache: store 1st-degree LinkedIn connections locally
    # so we don't need to re-fetch from Unipile API every time.
    try:
        conn.execute("SELECT 1 FROM connections LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS connections (
                id              TEXT PRIMARY KEY,
                account_id      TEXT NOT NULL,
                provider_id     TEXT NOT NULL,
                public_id       TEXT DEFAULT '',
                name            TEXT DEFAULT '',
                headline        TEXT DEFAULT '',
                network_distance TEXT DEFAULT 'FIRST_DEGREE',
                synced_at       INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                UNIQUE(account_id, provider_id)
            );
            CREATE INDEX IF NOT EXISTS idx_connections_account ON connections(account_id);
            CREATE INDEX IF NOT EXISTS idx_connections_provider ON connections(provider_id);
            CREATE INDEX IF NOT EXISTS idx_connections_public_id ON connections(public_id);
        """)
        conn.commit()
        logger.info("Migration: added connections table")

    # ── Connections table v2: add searchable fields for local connection search ──
    for col, ctype in [
        ("company", "TEXT DEFAULT ''"),
        ("location", "TEXT DEFAULT ''"),
        ("profile_url", "TEXT DEFAULT ''"),
        ("profile_json", "TEXT DEFAULT ''"),
    ]:
        try:
            conn.execute(f"ALTER TABLE connections ADD COLUMN {col} {ctype}")
            conn.commit()
            logger.info("Migration: added %s to connections", col)
        except sqlite3.OperationalError:
            pass

    for idx_sql in [
        "CREATE INDEX IF NOT EXISTS idx_connections_name ON connections(name COLLATE NOCASE)",
        "CREATE INDEX IF NOT EXISTS idx_connections_company ON connections(company COLLATE NOCASE)",
        "CREATE INDEX IF NOT EXISTS idx_connections_location ON connections(location COLLATE NOCASE)",
    ]:
        try:
            conn.execute(idx_sql)
            conn.commit()
        except sqlite3.OperationalError:
            pass

    # ── Post Intelligence v2: expanded post columns ──
    for col, ctype in [
        ("hashtags", "TEXT"),
        ("media_type", "TEXT"),
        ("media_url", "TEXT"),
        ("language", "TEXT"),
        ("visibility", "TEXT"),
        ("engagement_rate", "REAL"),
        ("author_followers", "INTEGER"),
        ("reactions_breakdown", "TEXT"),
        ("reposts_count", "INTEGER DEFAULT 0"),
        ("is_repost", "INTEGER DEFAULT 0"),
        ("original_post_id", "TEXT"),
    ]:
        try:
            conn.execute(f"ALTER TABLE posts ADD COLUMN {col} {ctype}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

    # ── Post Intelligence Phase 5: impressions_count column ──
    try:
        conn.execute("ALTER TABLE posts ADD COLUMN impressions_count INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists

    # ── Post metric snapshots: add impressions column ──
    try:
        conn.execute("ALTER TABLE post_metric_snapshots ADD COLUMN impressions INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists

    # ── Post metric snapshots (time-series tracking) ──
    try:
        conn.execute("SELECT 1 FROM post_metric_snapshots LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS post_metric_snapshots (
                id          TEXT PRIMARY KEY,
                post_id     TEXT NOT NULL,
                likes       INTEGER DEFAULT 0,
                comments    INTEGER DEFAULT 0,
                reposts     INTEGER DEFAULT 0,
                snapshot_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_snapshots_post ON post_metric_snapshots(post_id);
            CREATE INDEX IF NOT EXISTS idx_snapshots_at ON post_metric_snapshots(snapshot_at);
        """)
        conn.commit()
        logger.info("Migration: added post_metric_snapshots table")

    # ── Contact research pipeline columns ──
    for col, ctype in [
        ("research_status", "TEXT DEFAULT 'pending'"),
        ("research_completed_at", "INTEGER"),
        ("research_summary", "TEXT"),
    ]:
        try:
            conn.execute(f"ALTER TABLE contacts ADD COLUMN {col} {ctype}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

    # ── Signal improvements: watchlist_id, user_feedback, experiment_variant ──
    for col, ctype in [
        ("watchlist_id", "TEXT"),
        ("user_feedback", "TEXT"),
        ("feedback_at", "INTEGER"),
        ("experiment_variant", "TEXT"),
    ]:
        try:
            conn.execute(f"ALTER TABLE signals ADD COLUMN {col} {ctype}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_signals_watchlist ON signals(watchlist_id)"
    )
    conn.commit()

    # ── Watchlist auto-tuning columns ──
    for col, ctype in [
        ("auto_tuned_at", "INTEGER"),
        ("disabled_keywords", "TEXT DEFAULT '[]'"),
    ]:
        try:
            conn.execute(f"ALTER TABLE signal_watchlists ADD COLUMN {col} {ctype}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists

    # ── Collection metrics table (observability) ──
    try:
        conn.execute("SELECT 1 FROM collection_metrics LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS collection_metrics (
                id                TEXT PRIMARY KEY,
                collector_type    TEXT NOT NULL,
                account_id        TEXT,
                contacts_scanned  INTEGER DEFAULT 0,
                posts_collected   INTEGER DEFAULT 0,
                posts_analyzed    INTEGER DEFAULT 0,
                signals_created   INTEGER DEFAULT 0,
                errors            INTEGER DEFAULT 0,
                api_calls         INTEGER DEFAULT 0,
                duration_ms       INTEGER DEFAULT 0,
                error_details     TEXT,
                run_at            INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_collection_metrics_type ON collection_metrics(collector_type);
            CREATE INDEX IF NOT EXISTS idx_collection_metrics_at ON collection_metrics(run_at);
        """)
        conn.commit()
        logger.info("Migration: added collection_metrics table")

    # ── Signal threshold A/B testing ──
    try:
        conn.execute("SELECT 1 FROM signal_experiments LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS signal_experiments (
                id                TEXT PRIMARY KEY,
                campaign_id       TEXT NOT NULL,
                experiment_type   TEXT DEFAULT 'threshold',
                control_config    TEXT NOT NULL,
                treatment_config  TEXT NOT NULL,
                status            TEXT DEFAULT 'running',
                started_at        INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                completed_at      INTEGER,
                result_json       TEXT,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            );
            CREATE INDEX IF NOT EXISTS idx_signal_experiments_campaign ON signal_experiments(campaign_id);
            CREATE INDEX IF NOT EXISTS idx_signal_experiments_status ON signal_experiments(status);
        """)
        conn.commit()
        logger.info("Migration: added signal_experiments table")

    # ── Company posts tracked table (Phase 2 intent expansion) ──
    try:
        conn.execute("SELECT 1 FROM company_posts_tracked LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS company_posts_tracked (
                id                   TEXT PRIMARY KEY,
                watchlist_id         TEXT NOT NULL,
                post_id              TEXT NOT NULL,
                post_text            TEXT,
                last_checked_at      INTEGER,
                known_commenters     TEXT DEFAULT '[]',
                known_reactors       TEXT DEFAULT '[]',
                created_at           INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                FOREIGN KEY (watchlist_id) REFERENCES signal_watchlists(id)
            );
            CREATE INDEX IF NOT EXISTS idx_cpt_watchlist ON company_posts_tracked(watchlist_id);
            CREATE INDEX IF NOT EXISTS idx_cpt_post_id ON company_posts_tracked(post_id);
        """)
        conn.commit()
        logger.info("Migration: added company_posts_tracked table")

    # ── Composite indexes for signal_exists() performance ──
    for idx_sql in [
        "CREATE INDEX IF NOT EXISTS idx_signals_type_post_id ON signals(signal_type, post_id)",
        "CREATE INDEX IF NOT EXISTS idx_signals_type_linkedin_id ON signals(signal_type, linkedin_id)",
    ]:
        conn.execute(idx_sql)
    conn.commit()

    # Global contact base: backfill from existing campaign contacts
    _backfill_global_contacts(conn)

    # Inbound Pipeline v2 + delete message support
    # (was previously inside _backfill_global_contacts by mistake)
    _migrate_inbound_v2_and_delete_support(conn)

    # v0.10.131: Deduplicate outreaches — keep oldest per (campaign_id, contact_id),
    # delete duplicates, then add unique index to prevent future duplicates.
    try:
        row = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='index' AND name='idx_outreaches_campaign_contact'"
        ).fetchone()
        if not row:
            # Delete duplicate outreaches, keeping the one with the smallest rowid per pair
            deleted = conn.execute("""
                DELETE FROM outreaches WHERE rowid NOT IN (
                    SELECT MIN(rowid) FROM outreaches
                    GROUP BY campaign_id, contact_id
                )
            """).rowcount
            if deleted:
                logger.info("Migration: removed %d duplicate outreach records", deleted)
            conn.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_outreaches_campaign_contact
                    ON outreaches(campaign_id, contact_id)
            """)
            conn.commit()
            logger.info("Migration: added unique index idx_outreaches_campaign_contact")
    except Exception as e:
        logger.warning("Migration: outreach dedup failed: %s", e)


def _backfill_global_contacts(conn: sqlite3.Connection) -> None:
    """One-time backfill: create global_contacts from existing campaign contacts.

    Groups by linkedin_id, picks best data (most recent, highest fit_score),
    and links all campaign contacts via global_contact_id.
    """
    import uuid as _uuid

    # Check if backfill already ran (any global contacts exist)
    row = conn.execute("SELECT COUNT(*) as cnt FROM global_contacts").fetchone()
    if row and row[0] > 0:
        return

    # Check if there are any contacts to backfill
    contact_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM contacts WHERE global_contact_id IS NULL"
    ).fetchone()
    if not contact_count or contact_count[0] == 0:
        return

    now = int(time.time())
    backfilled = 0

    # Group contacts by linkedin_id (non-empty ones)
    grouped_rows = conn.execute("""
        SELECT linkedin_id,
               GROUP_CONCAT(id) as contact_ids,
               MAX(name) as name,
               MAX(title) as title,
               MAX(company) as company,
               MAX(linkedin_url) as linkedin_url,
               MAX(fit_score) as fit_score,
               MAX(profile_json) as profile_json,
               MAX(analysis_json) as analysis_json,
               MIN(campaign_id) as first_campaign_id,
               COUNT(*) as campaign_count,
               MIN(created_at) as first_seen,
               MAX(source) as source
        FROM contacts
        WHERE linkedin_id IS NOT NULL AND linkedin_id != ''
        GROUP BY linkedin_id
    """).fetchall()

    for row in grouped_rows:
        gid = str(_uuid.uuid4())
        linkedin_id = row["linkedin_id"]

        # Derive lifecycle from best outreach status across all campaigns
        best_status = conn.execute("""
            SELECT o.status, o.invited_at, MAX(o.updated_at) as last_interaction
            FROM outreaches o
            JOIN contacts c ON o.contact_id = c.id
            WHERE c.linkedin_id = ?
            ORDER BY
                CASE o.status
                    WHEN 'closed_happy' THEN 1
                    WHEN 'hot_lead' THEN 2
                    WHEN 'replied' THEN 3
                    WHEN 'connected' THEN 4
                    WHEN 'messaged' THEN 4
                    WHEN 'invited' THEN 5
                    ELSE 6
                END
            LIMIT 1
        """, (linkedin_id,)).fetchone()

        lifecycle = "prospect"
        first_contacted = None
        last_interaction = None
        if best_status:
            s = best_status["status"]
            if s == "closed_happy":
                lifecycle = "customer"
            elif s == "closed_unhappy":
                lifecycle = "lost"
            elif s in ("replied", "hot_lead"):
                lifecycle = "engaged"
            elif s in ("connected", "messaged"):
                lifecycle = "connected"
            elif s == "invited":
                lifecycle = "contacted"
            first_contacted = best_status["invited_at"]
            last_interaction = best_status["last_interaction"]

        conn.execute("""
            INSERT INTO global_contacts
                (id, linkedin_id, linkedin_url, name, title, company,
                 profile_json, analysis_json, fit_score,
                 lifecycle_stage, source, first_campaign_id, total_campaigns,
                 first_contacted_at, last_interaction_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            gid, linkedin_id, row["linkedin_url"],
            row["name"] or "", row["title"] or "", row["company"] or "",
            row["profile_json"], row["analysis_json"],
            row["fit_score"] or 0.0,
            lifecycle, row["source"] or "search",
            row["first_campaign_id"],
            row["campaign_count"],
            first_contacted, last_interaction,
            row["first_seen"] or now, now,
        ))

        # Link all campaign contacts to this global contact
        contact_ids = row["contact_ids"].split(",")
        for cid in contact_ids:
            conn.execute(
                "UPDATE contacts SET global_contact_id = ? WHERE id = ?",
                (gid, cid.strip()),
            )
        backfilled += 1

    # Handle contacts without linkedin_id (name-only)
    orphan_rows = conn.execute("""
        SELECT id, name, title, company, linkedin_url, fit_score,
               profile_json, analysis_json, campaign_id, source, created_at
        FROM contacts
        WHERE (linkedin_id IS NULL OR linkedin_id = '')
          AND global_contact_id IS NULL
    """).fetchall()

    for row in orphan_rows:
        gid = str(_uuid.uuid4())
        conn.execute("""
            INSERT INTO global_contacts
                (id, name, title, company, linkedin_url,
                 profile_json, analysis_json, fit_score,
                 lifecycle_stage, source, first_campaign_id, total_campaigns,
                 created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'prospect', ?, ?, 1, ?, ?)
        """, (
            gid, row["name"] or "", row["title"] or "", row["company"] or "",
            row["linkedin_url"],
            row["profile_json"], row["analysis_json"],
            row["fit_score"] or 0.0,
            row["source"] or "search", row["campaign_id"],
            row["created_at"] or now, now,
        ))
        conn.execute(
            "UPDATE contacts SET global_contact_id = ? WHERE id = ?",
            (gid, row["id"]),
        )
        backfilled += 1

    if backfilled > 0:
        conn.commit()
        logger.info("Migration: backfilled %d global contacts from existing campaign contacts", backfilled)


def _migrate_inbound_v2_and_delete_support(conn: sqlite3.Connection) -> None:
    """Inbound Pipeline v2 columns + delete message support.

    Previously these were inside _backfill_global_contacts() by mistake,
    so they were skipped on DBs that already had global contacts.
    """
    # ── Inbound Pipeline v2: classify-first columns ──
    for col, ctype in [
        ("invitation_id", "TEXT"),
        ("actioned_at", "INTEGER"),
        ("decline_reason", "TEXT"),
        ("message_id", "TEXT"),
        ("reaction_sent", "INTEGER DEFAULT 0"),
    ]:
        try:
            conn.execute(f"ALTER TABLE inbound_signals ADD COLUMN {col} {ctype}")
            conn.commit()
            logger.info("Migration: added %s to inbound_signals", col)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Inbound Pipeline v2: rename 'qualified' → 'classified' status
    try:
        updated = conn.execute(
            "UPDATE inbound_signals SET status = 'classified' WHERE status = 'qualified'"
        ).rowcount
        if updated:
            conn.commit()
            logger.info("Migration: renamed %d inbound_signals 'qualified' → 'classified'", updated)
    except sqlite3.OperationalError:
        pass

    # Inbound Pipeline v2: index on invitation_id
    try:
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_inbound_signals_invitation_id "
            "ON inbound_signals(invitation_id)"
        )
        conn.commit()
    except sqlite3.OperationalError:
        pass

    # Delete message support: track deleted messages and Unipile message IDs
    try:
        conn.execute("ALTER TABLE messages ADD COLUMN deleted_at INTEGER")
        conn.commit()
        logger.info("Migration: added deleted_at to messages")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        conn.execute("ALTER TABLE messages ADD COLUMN external_message_id TEXT")
        conn.commit()
        logger.info("Migration: added external_message_id to messages")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Signal optimization tables (self-tuning system)
    try:
        conn.execute("SELECT 1 FROM signal_weight_overrides LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS signal_weight_overrides (
                signal_type     TEXT PRIMARY KEY,
                weight          REAL NOT NULL,
                previous_weight REAL NOT NULL,
                source          TEXT NOT NULL DEFAULT 'auto',
                applied_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                applied_by      TEXT DEFAULT 'optimizer'
            );
            CREATE TABLE IF NOT EXISTS signal_threshold_overrides (
                threshold_name  TEXT PRIMARY KEY,
                value           REAL NOT NULL,
                previous_value  REAL NOT NULL,
                source          TEXT NOT NULL DEFAULT 'auto',
                applied_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                applied_by      TEXT DEFAULT 'optimizer'
            );
            CREATE TABLE IF NOT EXISTS optimization_history (
                id                TEXT PRIMARY KEY,
                optimization_type TEXT NOT NULL,
                target            TEXT NOT NULL,
                before_value      TEXT,
                after_value       TEXT,
                reason            TEXT,
                data_points       INTEGER DEFAULT 0,
                confidence        REAL DEFAULT 0.0,
                status            TEXT DEFAULT 'applied',
                applied_at        INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
                rolled_back_at    INTEGER,
                rolled_back_by    TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_opt_history_type ON optimization_history(optimization_type);
            CREATE INDEX IF NOT EXISTS idx_opt_history_applied ON optimization_history(applied_at);
        """)
        logger.info("Migration: added signal optimization tables")

    # Calendar events table (Google Calendar integration)
    try:
        conn.execute("SELECT 1 FROM calendar_events LIMIT 0")
    except sqlite3.OperationalError:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS calendar_events (
                id              TEXT PRIMARY KEY,
                outreach_id     TEXT REFERENCES outreaches(id),
                campaign_id     TEXT,
                google_event_id TEXT,
                event_link      TEXT,
                summary         TEXT,
                start_time      INTEGER NOT NULL,
                end_time        INTEGER NOT NULL,
                attendee_email  TEXT,
                attendee_name   TEXT,
                prospect_name   TEXT,
                status          TEXT DEFAULT 'created',
                created_at      INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
            );
            CREATE INDEX IF NOT EXISTS idx_cal_events_outreach ON calendar_events(outreach_id);
            CREATE INDEX IF NOT EXISTS idx_cal_events_campaign ON calendar_events(campaign_id);
        """)
        logger.info("Migration: added calendar_events table")


def reset_db() -> None:
    """Delete the database file entirely, creating a backup first."""
    path = config.db_path()
    if path.exists():
        try:
            from .backup import create_backup, rotate_backups

            create_backup("pre-reset")
            rotate_backups()
        except Exception as exc:
            logger.warning("Could not create pre-reset backup: %s", exc)
        path.unlink()
        logger.info("Database deleted")
