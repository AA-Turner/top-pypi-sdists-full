"""SQLite FTS5-backed memory service for persistent cross-session recall.

Implements ADK's BaseMemoryService interface using SQLite full-text search.
Zero external dependencies — works in frozen (PyInstaller) builds out of the box.

Storage location: ~/.ghost-pc/memory.db
Search: SQLite FTS5 with BM25 ranking
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

from google.adk.memory.base_memory_service import BaseMemoryService, SearchMemoryResponse
from google.adk.memory.memory_entry import MemoryEntry

if TYPE_CHECKING:
    from google.adk.sessions import Session

logger = logging.getLogger(__name__)

MAX_SEARCH_RESULTS = 5
MIN_DOC_LENGTH = 20
MAX_DOC_LENGTH = 2000

_SCHEMA = """\
CREATE TABLE IF NOT EXISTS memories (
    id        TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id   TEXT NOT NULL,
    role      TEXT NOT NULL DEFAULT 'unknown',
    author    TEXT NOT NULL DEFAULT 'unknown',
    content   TEXT NOT NULL,
    created_at REAL NOT NULL DEFAULT (julianday('now'))
);

CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    content,
    content='memories',
    content_rowid='rowid'
);

-- Triggers to keep FTS index in sync with the main table
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, content) VALUES (new.rowid, new.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content)
        VALUES ('delete', old.rowid, old.content);
END;

CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content)
        VALUES ('delete', old.rowid, old.content);
    INSERT INTO memories_fts(rowid, content) VALUES (new.rowid, new.content);
END;
"""


def _default_db_path() -> Path:
    """Return the default memory DB path inside GHOST_HOME."""
    from ghost_pc.config.schema import GHOST_HOME

    return GHOST_HOME / "memory.db"


class SQLiteMemoryService(BaseMemoryService):
    """Persistent memory using SQLite FTS5 full-text search.

    Stores conversation fragments from past sessions and retrieves
    relevant ones via BM25-ranked full-text search.  All data lives
    in a single ``memory.db`` file — no servers, no cloud, no extra deps.
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = Path(db_path or _default_db_path())
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(str(self._db_path))
        self._conn.executescript(_SCHEMA)
        self._conn.execute("PRAGMA journal_mode=WAL")

        count = self._conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        logger.info("SQLite memory initialized at %s (%d documents)", self._db_path, count)

    async def add_session_to_memory(self, session: Session) -> None:
        """Extract text from session events and store as documents."""
        if not session.events:
            return

        rows: list[tuple[str, str, str, str, str, str]] = []

        for i, event in enumerate(session.events):
            if not event.content or not event.content.parts:
                continue
            text_parts = [p.text for p in event.content.parts if p.text]
            if not text_parts:
                continue

            text = " ".join(text_parts)
            if len(text) < MIN_DOC_LENGTH:
                continue

            doc_id = f"{session.id}_{i}"
            rows.append(
                (
                    doc_id,
                    session.id,
                    session.user_id,
                    event.content.role or "unknown",
                    getattr(event, "author", "unknown"),
                    text[:MAX_DOC_LENGTH],
                )
            )

        if rows:
            self._conn.executemany(
                "INSERT OR REPLACE INTO memories (id, session_id, user_id, role, author, content)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                rows,
            )
            self._conn.commit()

            total = self._conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            logger.info(
                "Stored %d documents from session %s (total: %d)",
                len(rows),
                session.id,
                total,
            )

    async def search_memory(
        self,
        *,
        app_name: str,
        user_id: str,
        query: str,
    ) -> SearchMemoryResponse:
        """Search past sessions for relevant context using FTS5 + BM25 ranking."""
        from google.genai import types

        count = self._conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        if count == 0:
            return SearchMemoryResponse(memories=[])

        # Tokenize query for FTS5 — quote each word to avoid syntax errors
        words = query.split()
        if not words:
            return SearchMemoryResponse(memories=[])
        fts_query = " OR ".join(f'"{w}"' for w in words[:20])

        # BM25-ranked search scoped to the requesting user
        sql = """
            SELECT m.content, m.author
            FROM memories_fts fts
            JOIN memories m ON m.rowid = fts.rowid
            WHERE memories_fts MATCH ?
              AND m.user_id = ?
            ORDER BY bm25(memories_fts) ASC
            LIMIT ?
        """

        try:
            rows = self._conn.execute(sql, (fts_query, user_id, MAX_SEARCH_RESULTS)).fetchall()
        except sqlite3.OperationalError:
            # FTS query syntax issue — fall back to no results
            logger.debug("FTS5 query failed for: %s", fts_query, exc_info=True)
            return SearchMemoryResponse(memories=[])

        memories: list[MemoryEntry] = []
        for content, author in rows:
            memories.append(
                MemoryEntry(
                    content=types.Content(
                        role="user",
                        parts=[types.Part(text=f"[Memory] {content}")],
                    ),
                    author=author,
                    timestamp=None,
                )
            )

        return SearchMemoryResponse(memories=memories)
