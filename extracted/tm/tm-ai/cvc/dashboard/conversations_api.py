"""
Conversation history persistence — local SQLite store.

Stores every chat thread (user + assistant turns) keyed by workspace,
so users can revisit history scoped to one workspace ("just HydroPlus")
or see everything across all workspaces ("All").

Storage layout:

    ~/.cvc/conversations.db
        threads (id PK, workspace_path, title, created_at, updated_at,
                 persona_id, hostname)
        messages (id PK, thread_id FK, role, content, created_at)

Hostname column means: if a CVC gateway starts on the same machine, it
sees the same history; if synced to another machine later, history can
be filtered or merged by host.

Routes are mounted on the gateway via include_router(router).
"""

from __future__ import annotations

import logging
import socket
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

DB_PATH = Path.home() / ".cvc" / "conversations.db"
HOSTNAME = socket.gethostname()

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


# ── DB plumbing ─────────────────────────────────────────────────────────


def _ensure_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def _conn() -> Iterator[sqlite3.Connection]:
    _ensure_dir()
    c = sqlite3.connect(str(DB_PATH))
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()


def _init_schema() -> None:
    with _conn() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS threads (
                id           TEXT PRIMARY KEY,
                workspace_path TEXT NOT NULL,
                title        TEXT NOT NULL,
                persona_id   TEXT,
                hostname     TEXT NOT NULL,
                created_at   REAL NOT NULL,
                updated_at   REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_threads_ws
              ON threads(workspace_path, updated_at DESC);
            CREATE INDEX IF NOT EXISTS idx_threads_updated
              ON threads(updated_at DESC);

            CREATE TABLE IF NOT EXISTS messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id   TEXT NOT NULL,
                role        TEXT NOT NULL,
                content     TEXT NOT NULL,
                created_at  REAL NOT NULL,
                FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_messages_thread
              ON messages(thread_id, created_at);
            """
        )


_init_schema()


# ── Pydantic models ─────────────────────────────────────────────────────


class ThreadSummary(BaseModel):
    id: str
    workspace_path: str
    title: str
    persona_id: Optional[str] = None
    hostname: str
    created_at: float
    updated_at: float
    message_count: int = 0


class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system|tool)$")
    content: str
    created_at: Optional[float] = None


class ThreadDetail(ThreadSummary):
    messages: List[Message]


class CreateThreadRequest(BaseModel):
    workspace_path: str
    title: Optional[str] = None
    persona_id: Optional[str] = None
    first_message: Optional[Message] = None


class AppendMessageRequest(BaseModel):
    role: str
    content: str


class RenameThreadRequest(BaseModel):
    title: str


# ── Helpers ─────────────────────────────────────────────────────────────


def _derive_title(text: str, fallback: str = "New conversation") -> str:
    t = (text or "").strip().replace("\n", " ")
    if not t:
        return fallback
    return (t[:60] + "…") if len(t) > 60 else t


def _row_to_summary(row: sqlite3.Row, message_count: int = 0) -> ThreadSummary:
    return ThreadSummary(
        id=row["id"],
        workspace_path=row["workspace_path"],
        title=row["title"],
        persona_id=row["persona_id"],
        hostname=row["hostname"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        message_count=message_count,
    )


# ── Routes ──────────────────────────────────────────────────────────────


@router.get("", response_model=List[ThreadSummary])
def list_threads(
    workspace_path: Optional[str] = Query(
        None,
        description="If provided, only return threads from this workspace. "
        "Pass empty / omit for all-workspaces view.",
    ),
    limit: int = Query(200, ge=1, le=2000),
    offset: int = Query(0, ge=0),
) -> List[ThreadSummary]:
    """List conversation threads, optionally scoped to one workspace."""
    with _conn() as c:
        if workspace_path:
            cur = c.execute(
                """
                SELECT t.*, COUNT(m.id) AS message_count
                  FROM threads t
                  LEFT JOIN messages m ON m.thread_id = t.id
                 WHERE t.workspace_path = ?
                 GROUP BY t.id
                 ORDER BY t.updated_at DESC
                 LIMIT ? OFFSET ?
                """,
                (workspace_path, limit, offset),
            )
        else:
            cur = c.execute(
                """
                SELECT t.*, COUNT(m.id) AS message_count
                  FROM threads t
                  LEFT JOIN messages m ON m.thread_id = t.id
                 GROUP BY t.id
                 ORDER BY t.updated_at DESC
                 LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )
        return [_row_to_summary(r, r["message_count"]) for r in cur.fetchall()]


@router.get("/{thread_id}", response_model=ThreadDetail)
def get_thread(thread_id: str) -> ThreadDetail:
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM threads WHERE id = ?", (thread_id,)
        ).fetchone()
        if not row:
            raise HTTPException(404, f"Thread not found: {thread_id}")
        msgs = c.execute(
            "SELECT role, content, created_at FROM messages "
            "WHERE thread_id = ? ORDER BY created_at ASC, id ASC",
            (thread_id,),
        ).fetchall()
    summary = _row_to_summary(row, len(msgs))
    return ThreadDetail(
        **summary.model_dump(),
        messages=[
            Message(role=m["role"], content=m["content"], created_at=m["created_at"])
            for m in msgs
        ],
    )


@router.post("", response_model=ThreadSummary)
def create_thread(body: CreateThreadRequest) -> ThreadSummary:
    now = time.time()
    tid = uuid.uuid4().hex[:16]
    title = body.title or (
        _derive_title(body.first_message.content)
        if body.first_message
        else "New conversation"
    )
    with _conn() as c:
        c.execute(
            "INSERT INTO threads "
            "(id, workspace_path, title, persona_id, hostname, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tid, body.workspace_path, title, body.persona_id, HOSTNAME, now, now),
        )
        mc = 0
        if body.first_message:
            c.execute(
                "INSERT INTO messages (thread_id, role, content, created_at) "
                "VALUES (?, ?, ?, ?)",
                (tid, body.first_message.role, body.first_message.content, now),
            )
            mc = 1
        row = c.execute("SELECT * FROM threads WHERE id = ?", (tid,)).fetchone()
    return _row_to_summary(row, mc)


@router.post("/{thread_id}/messages", response_model=ThreadSummary)
def append_message(thread_id: str, body: AppendMessageRequest) -> ThreadSummary:
    now = time.time()
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM threads WHERE id = ?", (thread_id,)
        ).fetchone()
        if not row:
            raise HTTPException(404, f"Thread not found: {thread_id}")
        c.execute(
            "INSERT INTO messages (thread_id, role, content, created_at) "
            "VALUES (?, ?, ?, ?)",
            (thread_id, body.role, body.content, now),
        )
        c.execute(
            "UPDATE threads SET updated_at = ? WHERE id = ?", (now, thread_id)
        )
        mc = c.execute(
            "SELECT COUNT(*) AS n FROM messages WHERE thread_id = ?", (thread_id,)
        ).fetchone()["n"]
        row = c.execute("SELECT * FROM threads WHERE id = ?", (thread_id,)).fetchone()
    return _row_to_summary(row, mc)


@router.patch("/{thread_id}", response_model=ThreadSummary)
def rename_thread(thread_id: str, body: RenameThreadRequest) -> ThreadSummary:
    now = time.time()
    title = (body.title or "").strip() or "Untitled"
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM threads WHERE id = ?", (thread_id,)
        ).fetchone()
        if not row:
            raise HTTPException(404, f"Thread not found: {thread_id}")
        c.execute(
            "UPDATE threads SET title = ?, updated_at = ? WHERE id = ?",
            (title, now, thread_id),
        )
        mc = c.execute(
            "SELECT COUNT(*) AS n FROM messages WHERE thread_id = ?", (thread_id,)
        ).fetchone()["n"]
        row = c.execute("SELECT * FROM threads WHERE id = ?", (thread_id,)).fetchone()
    return _row_to_summary(row, mc)


@router.delete("/{thread_id}")
def delete_thread(thread_id: str) -> dict:
    with _conn() as c:
        cur = c.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
        c.execute("DELETE FROM messages WHERE thread_id = ?", (thread_id,))
    return {"status": "ok", "deleted": cur.rowcount}


@router.get("/_/stats")
def stats() -> dict:
    with _conn() as c:
        threads = c.execute("SELECT COUNT(*) AS n FROM threads").fetchone()["n"]
        messages = c.execute("SELECT COUNT(*) AS n FROM messages").fetchone()["n"]
        workspaces = c.execute(
            "SELECT workspace_path, COUNT(*) AS n FROM threads "
            "GROUP BY workspace_path ORDER BY n DESC"
        ).fetchall()
    return {
        "threads": threads,
        "messages": messages,
        "hostname": HOSTNAME,
        "db_path": str(DB_PATH),
        "by_workspace": [
            {"workspace_path": r["workspace_path"], "threads": r["n"]}
            for r in workspaces
        ],
    }
