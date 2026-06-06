"""Schema management, domain initialization, and migration for knowledge DB.

Extracted from knowledge.py — pure functions that receive db connection and
filesystem parameters instead of using self.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def ensure_schema(conn):
    """Create or migrate the knowledge DB schema (entries, FTS5, triggers)."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            domain TEXT NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            content_segmented TEXT DEFAULT '',
            code_example TEXT DEFAULT '',
            tags TEXT DEFAULT '[]',
            source TEXT DEFAULT '{}',
            severity TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'active',
            created_at TEXT NOT NULL,
            updated_at TEXT,
            stale_at TEXT,
            referenced_count INTEGER DEFAULT 0,
            last_referenced_at TEXT,
            last_referenced_by TEXT,
            type TEXT DEFAULT 'knowledge',
            steps TEXT DEFAULT NULL
        );
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id TEXT NOT NULL,
            task_id TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
    """)

    # Add missing columns to existing databases
    cols = {r[1] for r in conn.execute("PRAGMA table_info(entries)")}
    if "content_segmented" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN content_segmented TEXT DEFAULT ''")
    if "embedding" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN embedding BLOB DEFAULT NULL")
    if "type" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN type TEXT DEFAULT 'knowledge'")
    if "steps" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN steps TEXT DEFAULT NULL")
    if "benchmark" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN benchmark TEXT DEFAULT NULL")
    if "biz_context" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN biz_context TEXT DEFAULT NULL")
    if "effectiveness" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN effectiveness TEXT DEFAULT NULL")
    if "evidence" not in cols:
        conn.execute("ALTER TABLE entries ADD COLUMN evidence TEXT DEFAULT NULL")

    # Rebuild FTS5 with content_segmented column
    has_content_seg = False
    try:
        fts_cols = {r[1] for r in conn.execute("PRAGMA table_info(entries_fts)")}
        has_content_seg = "content_segmented" in fts_cols
    except sqlite3.OperationalError:
        pass

    if not has_content_seg:
        conn.execute("DROP TABLE IF EXISTS entries_fts")
        conn.execute(
            "CREATE VIRTUAL TABLE entries_fts USING fts5("
            "title, content, content_segmented, code_example, tags, "
            "content=entries, content_rowid=rowid)"
        )
        conn.execute(
            "INSERT INTO entries_fts(rowid, title, content, content_segmented, code_example, tags) "
            "SELECT rowid, title, content, content_segmented, code_example, tags FROM entries"
        )

    # Add indexes for common filter columns
    conn.execute("CREATE INDEX IF NOT EXISTS idx_entries_status ON entries(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_entries_biz_context ON entries(biz_context)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_entries_status_biz ON entries(status, biz_context)")

    # Version history table for tracking entry changes (#482)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entry_versions (
            version_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id TEXT NOT NULL,
            content TEXT NOT NULL,
            code_example TEXT DEFAULT '',
            tags TEXT DEFAULT '[]',
            source TEXT DEFAULT '{}',
            severity TEXT DEFAULT 'medium',
            snapshot_at TEXT NOT NULL,
            snapshot_reason TEXT DEFAULT 'upsert',
            evidence TEXT DEFAULT NULL,
            FOREIGN KEY (entry_id) REFERENCES entries(id)
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_versions_entry_id ON entry_versions(entry_id)"
    )
    # Add evidence column to existing entry_versions tables
    try:
        ver_cols = {r[1] for r in conn.execute("PRAGMA table_info(entry_versions)")}
        if "evidence" not in ver_cols:
            conn.execute("ALTER TABLE entry_versions ADD COLUMN evidence TEXT DEFAULT NULL")
    except Exception:
        pass

    # Rebuild triggers (idempotent)
    conn.executescript("""
        DROP TRIGGER IF EXISTS entries_ai;
        DROP TRIGGER IF EXISTS entries_ad;
        DROP TRIGGER IF EXISTS entries_au;
        CREATE TRIGGER entries_ai AFTER INSERT ON entries BEGIN
            INSERT INTO entries_fts(rowid, title, content, content_segmented, code_example, tags)
            VALUES (new.rowid, new.title, new.content, new.content_segmented, new.code_example, new.tags);
        END;
        CREATE TRIGGER entries_ad AFTER DELETE ON entries BEGIN
            INSERT INTO entries_fts(entries_fts, rowid, title, content, content_segmented, code_example, tags)
            VALUES ('delete', old.rowid, old.title, old.content, old.content_segmented, old.code_example, old.tags);
        END;
        CREATE TRIGGER entries_au AFTER UPDATE ON entries BEGIN
            INSERT INTO entries_fts(entries_fts, rowid, title, content, content_segmented, code_example, tags)
            VALUES ('delete', old.rowid, old.title, old.content, old.content_segmented, old.code_example, old.tags);
            INSERT INTO entries_fts(rowid, title, content, content_segmented, code_example, tags)
            VALUES (new.rowid, new.title, new.content, new.content_segmented, new.code_example, new.tags);
        END;
    """)


def ensure_domains(conn):
    """Ensure domain table populated and backfill segmented content + embeddings."""
    from kanban_framework.domain.knowledge_lazy import (
        DEFAULT_DOMAINS, _get_jieba, _segment, _embed, _get_embed_model,
    )

    conn.execute(
        "CREATE TABLE IF NOT EXISTS domains (name TEXT PRIMARY KEY, label TEXT, keywords TEXT)"
    )
    existing = {r[0] for r in conn.execute("SELECT name FROM domains")}
    for name, info in DEFAULT_DOMAINS.items():
        if name not in existing:
            conn.execute(
                "INSERT INTO domains(name, label, keywords) VALUES(?,?,?)",
                (name, info["label"], json.dumps(info["keywords"])),
            )

    # Backfill content_segmented for entries created before jieba integration
    if _get_jieba():
        blanks = conn.execute(
            "SELECT rowid, title, content, code_example FROM entries WHERE content_segmented=''"
        ).fetchall()
        if blanks:
            for row in blanks:
                seg = _segment(row[1]) + " " + _segment(row[2])
                if row[3]:
                    seg += " " + _segment(row[3])
                conn.execute(
                    "UPDATE entries SET content_segmented=? WHERE rowid=?",
                    (seg, row[0]),
                )
            conn.commit()
            # Rebuild FTS5 to pick up the new segmented content
            conn.execute("DELETE FROM entries_fts")
            conn.execute(
                "INSERT INTO entries_fts(rowid, title, content, content_segmented, code_example, tags) "
                "SELECT rowid, title, content, content_segmented, code_example, tags FROM entries"
            )

    # Backfill embeddings for entries created before fastembed integration
    model = _get_embed_model()
    if model is not None:
        blanks = conn.execute(
            "SELECT rowid, title, content FROM entries WHERE embedding IS NULL"
        ).fetchall()
        if blanks:
            for row in blanks:
                emb = _embed(row[1] + " " + row[2])
                if emb:
                    conn.execute(
                        "UPDATE entries SET embedding=? WHERE rowid=?",
                        (emb, row[0]),
                    )
            conn.commit()


def migrate_legacy_db(db_path: Path, scope: str, db_dir: Path) -> None:
    """Rename knowledge.db → knowledge-{scope}.db on first scope activation.

    One-time migration: when scope is configured and the scoped DB doesn't
    exist yet, but the default knowledge.db does, rename it so existing
    entries are preserved. Idempotent.
    """
    if not scope:
        return
    legacy = db_dir / "knowledge.db"
    if db_path.is_file() or not legacy.is_file():
        return
    try:
        legacy.rename(db_path)
    except OSError:
        try:
            import shutil
            shutil.copy2(str(legacy), str(db_path))
        except OSError:
            pass


def migrate_stale_at(conn) -> None:
    """Backfill stale_at for historical entries that have NULL stale_at.

    Sets stale_at = created_at + 90 days so existing entries get a reasonable
    default instead of silently staying active forever.
    """
    try:
        null_exists = conn.execute(
            "SELECT 1 FROM entries WHERE stale_at IS NULL LIMIT 1"
        ).fetchone()
        if null_exists:
            conn.execute(
                "UPDATE entries SET stale_at = datetime(created_at, '+90 days') "
                "WHERE stale_at IS NULL"
            )
            conn.commit()
    except Exception:
        pass  # Migration must not block startup
