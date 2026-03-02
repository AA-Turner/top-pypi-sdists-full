"""Database migration — create all tables for PostgreSQL or SQLite."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from salmalm.db.connection import OperationalError, get_connection

SCHEMA_STATEMENTS: tuple[str, ...] = (
    """CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        event TEXT NOT NULL,
        detail TEXT,
        prev_hash TEXT,
        hash TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS audit_log_v2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        event_type TEXT NOT NULL,
        session_id TEXT,
        detail TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS usage_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        model TEXT NOT NULL,
        input_tokens INTEGER,
        output_tokens INTEGER,
        cost REAL,
        user_id INTEGER
    )""",
    """CREATE TABLE IF NOT EXISTS usage_detail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        session_id TEXT,
        model TEXT NOT NULL,
        input_tokens INTEGER DEFAULT 0,
        output_tokens INTEGER DEFAULT 0,
        cost REAL DEFAULT 0.0,
        intent TEXT DEFAULT ''
    )""",
    """CREATE TABLE IF NOT EXISTS session_store (
        session_id TEXT PRIMARY KEY,
        messages TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        parent_session_id TEXT DEFAULT NULL,
        branch_index INTEGER DEFAULT NULL,
        title TEXT DEFAULT '',
        user_id INTEGER DEFAULT NULL,
        session_meta TEXT DEFAULT '{}'
    )""",
    """CREATE TABLE IF NOT EXISTS session_message_backup (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        messages_json TEXT NOT NULL,
        removed_at TEXT NOT NULL,
        reason TEXT DEFAULT 'rollback'
    )""",
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash BLOB NOT NULL DEFAULT x'',
        password_salt BLOB NOT NULL DEFAULT x'',
        role TEXT NOT NULL DEFAULT 'user',
        api_key TEXT UNIQUE,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        last_login TEXT,
        enabled INTEGER NOT NULL DEFAULT 1
    )""",
    """CREATE TABLE IF NOT EXISTS sessions (
        token_hash TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        attempted_at REAL NOT NULL,
        ip_address TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS ip_bans (
        ip TEXT PRIMARY KEY,
        violations INTEGER NOT NULL DEFAULT 0,
        first_at REAL NOT NULL,
        banned_until REAL NOT NULL DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS daily_quota (
        user_id TEXT NOT NULL,
        date TEXT NOT NULL,
        tokens INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (user_id, date)
    )""",
    """CREATE TABLE IF NOT EXISTS revoked_tokens (
        jti TEXT PRIMARY KEY,
        revoked_at REAL NOT NULL,
        expires_at REAL NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS user_revocations (
        user_id TEXT PRIMARY KEY,
        revoked_after REAL NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS user_quotas (
        user_id INTEGER PRIMARY KEY,
        daily_limit REAL NOT NULL DEFAULT 5.0,
        monthly_limit REAL NOT NULL DEFAULT 50.0,
        current_daily REAL NOT NULL DEFAULT 0.0,
        current_monthly REAL NOT NULL DEFAULT 0.0,
        last_daily_reset TEXT,
        last_monthly_reset TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        model_preference TEXT DEFAULT 'auto',
        persona TEXT DEFAULT 'default',
        routing_config TEXT DEFAULT '{}',
        tts_enabled INTEGER DEFAULT 0,
        tts_voice TEXT DEFAULT 'alloy',
        settings_json TEXT DEFAULT '{}'
    )""",
    """CREATE TABLE IF NOT EXISTS telegram_users (
        chat_id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        username TEXT,
        registered_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS multi_tenant_config (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS compaction_summaries (
        session_id TEXT PRIMARY KEY,
        summary TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS bookmarks (
        session_id TEXT NOT NULL,
        message_index INTEGER NOT NULL,
        title TEXT,
        note TEXT,
        tags TEXT,
        created_at TEXT NOT NULL,
        PRIMARY KEY (session_id, message_index)
    )""",
    """CREATE TABLE IF NOT EXISTS session_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        color TEXT DEFAULT '',
        sort_order INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS uptime_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT NOT NULL,
        end_time TEXT,
        duration_sec REAL,
        reason TEXT DEFAULT 'unknown'
    )""",
    """CREATE TABLE IF NOT EXISTS thoughts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        tags TEXT DEFAULT '',
        mood TEXT DEFAULT 'neutral',
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS capsules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_note TEXT NOT NULL,
        delivery_date TEXT NOT NULL,
        created_at TEXT NOT NULL,
        delivered INTEGER DEFAULT 0,
        delivery_channel TEXT DEFAULT ''
    )""",
    """CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL,
        active INTEGER DEFAULT 1
    )""",
    """CREATE TABLE IF NOT EXISTS habit_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT NOT NULL,
        check_date TEXT NOT NULL,
        checked_at TEXT NOT NULL,
        UNIQUE(habit_name, check_date)
    )""",
    """CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        content TEXT NOT NULL,
        mood TEXT DEFAULT 'neutral',
        mood_score REAL DEFAULT 0.5,
        auto_generated INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS quick_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        commands TEXT NOT NULL,
        description TEXT DEFAULT '',
        usage_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS play_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang TEXT NOT NULL,
        code TEXT NOT NULL,
        output TEXT,
        error TEXT,
        exit_code INTEGER,
        exec_time_ms REAL,
        memory_kb INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        line_start INTEGER NOT NULL,
        line_end INTEGER NOT NULL,
        text TEXT NOT NULL,
        tokens TEXT NOT NULL,
        token_count INTEGER NOT NULL,
        mtime REAL NOT NULL,
        hash TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS doc_freq (
        term TEXT PRIMARY KEY,
        df INTEGER NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS tfidf_vectors (
        chunk_id INTEGER PRIMARY KEY,
        vector TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS rag_embeddings (
        chunk_hash TEXT PRIMARY KEY,
        embedding TEXT NOT NULL,
        provider TEXT,
        dimensions INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS notes (
        id TEXT PRIMARY KEY,
        content TEXT NOT NULL,
        tags TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS expenses (
        id TEXT PRIMARY KEY,
        amount REAL NOT NULL,
        category TEXT DEFAULT '기타',
        description TEXT DEFAULT '',
        date TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS saved_links (
        id TEXT PRIMARY KEY,
        url TEXT NOT NULL,
        title TEXT DEFAULT '',
        summary TEXT DEFAULT '',
        tags TEXT DEFAULT '',
        content TEXT DEFAULT '',
        saved_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS pomodoro_sessions (
        id TEXT PRIMARY KEY,
        started_at TEXT NOT NULL,
        ended_at TEXT,
        type TEXT DEFAULT 'focus',
        completed INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS message_alternatives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        message_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        model TEXT DEFAULT '',
        is_active INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS vault_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        category TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )""",
)

MIGRATIONS: tuple[str, ...] = (
    "ALTER TABLE usage_stats ADD COLUMN user_id INTEGER",
    "ALTER TABLE session_store ADD COLUMN parent_session_id TEXT DEFAULT NULL",
    "ALTER TABLE session_store ADD COLUMN branch_index INTEGER DEFAULT NULL",
    "ALTER TABLE session_store ADD COLUMN title TEXT DEFAULT ''",
    "ALTER TABLE session_store ADD COLUMN user_id INTEGER DEFAULT NULL",
    "ALTER TABLE session_store ADD COLUMN session_meta TEXT DEFAULT '{}'",
    "ALTER TABLE session_store ADD COLUMN group_id INTEGER DEFAULT NULL",
)


def apply_schema(conn, statements: Iterable[str] = SCHEMA_STATEMENTS) -> None:
    for stmt in statements:
        conn.execute(stmt)
    for mig in MIGRATIONS:
        try:
            conn.execute(mig)
        except OperationalError:
            pass
    conn.commit()


def migrate(db_path: Path | str | None = None) -> None:
    conn = get_connection(db_path)
    try:
        apply_schema(conn)
    finally:
        conn.close()
