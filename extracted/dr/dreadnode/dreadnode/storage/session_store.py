from __future__ import annotations

import json
import sqlite3
import threading
import typing as t
from dataclasses import dataclass
from datetime import UTC, datetime

if t.TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from dreadnode.generators.message import Message


def _json_dumps(value: t.Any) -> str:
    return json.dumps(value, default=str, ensure_ascii=False, sort_keys=True)


def _parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now(UTC)
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)


@dataclass(slots=True)
class SessionRecord:
    session_id: str
    model: str
    project: str | None
    capability: str | None
    agent: str | None
    title: str | None
    created_at: datetime
    updated_at: datetime
    message_count: int
    trajectory: dict[str, t.Any] | None


@dataclass(slots=True)
class MessageSearchResult:
    session_id: str
    message_id: str
    seq: int
    role: str
    content: str
    snippet: str


class SessionStore:
    """SQLite-backed session metadata and message index with FTS5 search."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def _init_db(self) -> None:
        with self._lock, self._connect() as conn:
            conn.executescript(
                """
                PRAGMA journal_mode = WAL;
                PRAGMA synchronous = NORMAL;

                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    model TEXT NOT NULL,
                    project TEXT,
                    capability TEXT,
                    agent TEXT,
                    title TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    message_count INTEGER NOT NULL DEFAULT 0,
                    trajectory_json TEXT
                );

                CREATE TABLE IF NOT EXISTS messages (
                    session_id TEXT NOT NULL,
                    seq INTEGER NOT NULL,
                    message_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL DEFAULT '',
                    tool_call_id TEXT,
                    tool_calls_json TEXT,
                    metadata_json TEXT,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (session_id, seq),
                    UNIQUE (session_id, message_id),
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_messages_session_created_at
                    ON messages(session_id, created_at);

                CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
                    session_id UNINDEXED,
                    message_id UNINDEXED,
                    role UNINDEXED,
                    content,
                    tokenize = 'unicode61'
                );
                """
            )

    def upsert_session(
        self,
        *,
        session_id: str,
        model: str,
        project: str | None,
        capability: str | None,
        agent: str | None,
        title: str | None,
        created_at: datetime,
        updated_at: datetime | None = None,
        message_count: int = 0,
        trajectory: dict[str, t.Any] | None = None,
    ) -> None:
        updated_at = updated_at or datetime.now(UTC)
        trajectory_json = _json_dumps(trajectory) if trajectory is not None else None
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sessions (
                    session_id,
                    model,
                    project,
                    capability,
                    agent,
                    title,
                    created_at,
                    updated_at,
                    message_count,
                    trajectory_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    model = excluded.model,
                    project = excluded.project,
                    capability = excluded.capability,
                    agent = excluded.agent,
                    title = excluded.title,
                    updated_at = excluded.updated_at,
                    message_count = excluded.message_count,
                    trajectory_json = excluded.trajectory_json
                """,
                (
                    session_id,
                    model,
                    project,
                    capability,
                    agent,
                    title,
                    created_at.isoformat(),
                    updated_at.isoformat(),
                    message_count,
                    trajectory_json,
                ),
            )

    def replace_messages(self, session_id: str, messages: Sequence[Message]) -> None:
        timestamp = datetime.now(UTC).isoformat()
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM messages_fts WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))

            for seq, message in enumerate(messages):
                tool_calls_json = None
                if message.tool_calls:
                    tool_calls_json = _json_dumps(
                        [
                            tool_call.model_dump(mode="json")
                            if hasattr(tool_call, "model_dump")
                            else tool_call
                            for tool_call in message.tool_calls
                        ]
                    )

                metadata_json = _json_dumps(message.metadata) if message.metadata else None
                message_id = str(getattr(message, "uuid", f"{session_id}:{seq}"))
                role = str(message.role)
                content = message.content or ""

                conn.execute(
                    """
                    INSERT INTO messages (
                        session_id,
                        seq,
                        message_id,
                        role,
                        content,
                        tool_call_id,
                        tool_calls_json,
                        metadata_json,
                        created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session_id,
                        seq,
                        message_id,
                        role,
                        content,
                        message.tool_call_id,
                        tool_calls_json,
                        metadata_json,
                        timestamp,
                    ),
                )
                conn.execute(
                    """
                    INSERT INTO messages_fts (session_id, message_id, role, content)
                    VALUES (?, ?, ?, ?)
                    """,
                    (session_id, message_id, role, content),
                )

    def persist_session(
        self,
        *,
        session_id: str,
        model: str,
        project: str | None,
        capability: str | None,
        agent: str | None,
        title: str | None,
        created_at: datetime,
        updated_at: datetime | None = None,
        message_count: int = 0,
        trajectory: dict[str, t.Any] | None = None,
        messages: Sequence[Message] | None = None,
    ) -> None:
        """Atomically persist session metadata and messages in one transaction."""
        updated_at = updated_at or datetime.now(UTC)
        trajectory_json = _json_dumps(trajectory) if trajectory is not None else None
        timestamp = datetime.now(UTC).isoformat()

        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sessions (
                    session_id, model, project, capability, agent, title,
                    created_at, updated_at, message_count, trajectory_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    model = excluded.model,
                    project = excluded.project,
                    capability = excluded.capability,
                    agent = excluded.agent,
                    title = excluded.title,
                    updated_at = excluded.updated_at,
                    message_count = excluded.message_count,
                    trajectory_json = excluded.trajectory_json
                """,
                (
                    session_id,
                    model,
                    project,
                    capability,
                    agent,
                    title,
                    created_at.isoformat(),
                    updated_at.isoformat(),
                    message_count,
                    trajectory_json,
                ),
            )

            if messages is not None:
                for seq, message in enumerate(messages):
                    tool_calls_json = None
                    if message.tool_calls:
                        tool_calls_json = _json_dumps(
                            [
                                tool_call.model_dump(mode="json")
                                if hasattr(tool_call, "model_dump")
                                else tool_call
                                for tool_call in message.tool_calls
                            ]
                        )
                    metadata_json = _json_dumps(message.metadata) if message.metadata else None
                    message_id = str(getattr(message, "uuid", f"{session_id}:{seq}"))
                    role = str(message.role)
                    content = message.content or ""

                    conn.execute(
                        """
                        INSERT INTO messages (
                            session_id, seq, message_id, role, content,
                            tool_call_id, tool_calls_json, metadata_json, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(session_id, message_id) DO UPDATE SET
                            seq = excluded.seq,
                            content = excluded.content,
                            tool_call_id = excluded.tool_call_id,
                            tool_calls_json = excluded.tool_calls_json,
                            metadata_json = excluded.metadata_json
                        """,
                        (
                            session_id,
                            seq,
                            message_id,
                            role,
                            content,
                            message.tool_call_id,
                            tool_calls_json,
                            metadata_json,
                            timestamp,
                        ),
                    )
                    conn.execute(
                        "DELETE FROM messages_fts WHERE session_id = ? AND message_id = ?",
                        (session_id, message_id),
                    )
                    conn.execute(
                        "INSERT INTO messages_fts (session_id, message_id, role, content) VALUES (?, ?, ?, ?)",
                        (session_id, message_id, role, content),
                    )

                # Remove orphan rows beyond new message count (handles compaction/reset)
                conn.execute(
                    "DELETE FROM messages WHERE session_id = ? AND seq >= ?",
                    (session_id, len(messages)),
                )
                conn.execute(
                    """DELETE FROM messages_fts WHERE session_id = ? AND message_id NOT IN (
                        SELECT message_id FROM messages WHERE session_id = ?
                    )""",
                    (session_id, session_id),
                )

    def get_session(self, session_id: str) -> SessionRecord | None:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                    session_id,
                    model,
                    project,
                    capability,
                    agent,
                    title,
                    created_at,
                    updated_at,
                    message_count,
                    trajectory_json
                FROM sessions
                WHERE session_id = ?
                """,
                (session_id,),
            ).fetchone()
        return self._row_to_session(row) if row is not None else None

    def list_sessions(self, *, limit: int | None = None) -> list[SessionRecord]:
        query = """
            SELECT
                session_id,
                model,
                project,
                capability,
                agent,
                title,
                created_at,
                updated_at,
                message_count,
                trajectory_json
            FROM sessions
            ORDER BY updated_at DESC, created_at DESC
        """
        params: tuple[t.Any, ...] = ()
        if limit is not None:
            query += " LIMIT ?"
            params = (limit,)
        with self._lock, self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_session(row) for row in rows]

    def first_user_message(self, session_id: str, *, max_len: int = 200) -> str | None:
        """Return the content of the first user message in a session, truncated."""
        with self._lock, self._connect() as conn:
            row = conn.execute(
                """
                SELECT content FROM messages
                WHERE session_id = ? AND role = 'user'
                ORDER BY seq ASC LIMIT 1
                """,
                (session_id,),
            ).fetchone()
        if row is None:
            return None
        text = (row["content"] or "").strip().replace("\n", " ")
        if len(text) > max_len:
            return text[: max_len - 1] + "\u2026"
        return text or None

    def first_user_messages(self, session_ids: list[str], *, max_len: int = 200) -> dict[str, str]:
        """Batch-fetch first user message for multiple sessions."""
        if not session_ids:
            return {}
        placeholders = ",".join("?" for _ in session_ids)
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT session_id, content FROM messages
                WHERE rowid IN (
                    SELECT MIN(rowid) FROM messages
                    WHERE session_id IN ({placeholders}) AND role = 'user'
                    GROUP BY session_id
                )
                """,  # noqa: S608 — placeholders are parameterised "?" markers
                session_ids,
            ).fetchall()
        result: dict[str, str] = {}
        for row in rows:
            text = (row["content"] or "").strip().replace("\n", " ")
            if len(text) > max_len:
                text = text[: max_len - 1] + "\u2026"
            if text:
                result[row["session_id"]] = text
        return result

    def delete_session(self, session_id: str) -> bool:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM messages_fts WHERE session_id = ?", (session_id,))
            cursor = conn.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            return cursor.rowcount > 0

    def search_messages(
        self,
        query: str,
        *,
        session_id: str | None = None,
        limit: int = 20,
    ) -> list[MessageSearchResult]:
        if not query.strip():
            return []

        sql = """
            SELECT
                m.session_id,
                m.message_id,
                m.seq,
                m.role,
                m.content,
                highlight(messages_fts, 3, '[', ']') AS snippet
            FROM messages_fts
            JOIN messages AS m
              ON m.session_id = messages_fts.session_id
             AND m.message_id = messages_fts.message_id
            WHERE messages_fts MATCH ?
        """
        params: list[t.Any] = [query]
        if session_id is not None:
            sql += " AND m.session_id = ?"
            params.append(session_id)
        sql += " ORDER BY bm25(messages_fts), m.seq ASC LIMIT ?"
        params.append(limit)

        with self._lock, self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [
            MessageSearchResult(
                session_id=row["session_id"],
                message_id=row["message_id"],
                seq=row["seq"],
                role=row["role"],
                content=row["content"],
                snippet=row["snippet"] or row["content"],
            )
            for row in rows
        ]

    def _row_to_session(self, row: sqlite3.Row) -> SessionRecord:
        trajectory = None
        if row["trajectory_json"]:
            trajectory = t.cast("dict[str, t.Any]", json.loads(row["trajectory_json"]))
        return SessionRecord(
            session_id=t.cast("str", row["session_id"]),
            model=t.cast("str", row["model"]),
            project=t.cast("str | None", row["project"]),
            capability=t.cast("str | None", row["capability"]),
            agent=t.cast("str | None", row["agent"]),
            title=t.cast("str | None", row["title"]),
            created_at=_parse_datetime(t.cast("str | None", row["created_at"])),
            updated_at=_parse_datetime(t.cast("str | None", row["updated_at"])),
            message_count=int(row["message_count"]),
            trajectory=trajectory,
        )
