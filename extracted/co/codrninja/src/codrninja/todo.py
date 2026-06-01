"""Session-scoped todo tracking for codrninja."""

import os
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional


TODO_DB_PATH = os.path.expanduser("~/.codrninja/todos.db")
VALID_STATUSES = {"pending", "done", "cancelled"}


@dataclass
class TodoItem:
    """Represents a persisted todo item."""

    id: str
    task: str
    status: str
    created_at: str
    completed_at: Optional[str]
    session_id: str


class TodoManager:
    """Manage session-scoped todos backed by SQLite."""

    def __init__(self, db_path: str = TODO_DB_PATH):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        self._cleanup_old_items()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    task TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_todos_session_id ON todos(session_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at)"
            )
            conn.commit()

    def _cleanup_old_items(self):
        cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        with self._connect() as conn:
            conn.execute("DELETE FROM todos WHERE created_at < ?", (cutoff,))
            conn.commit()

    def _row_to_item(self, row: sqlite3.Row) -> TodoItem:
        return TodoItem(
            id=row["id"],
            session_id=row["session_id"],
            task=row["task"],
            status=row["status"],
            created_at=row["created_at"],
            completed_at=row["completed_at"],
        )

    def add(self, task: str, session_id: str) -> str:
        todo_id = str(uuid.uuid4())[:8]
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO todos (id, session_id, task, status, created_at, completed_at) VALUES (?, ?, ?, ?, ?, ?)",
                (todo_id, session_id, task, "pending", created_at, None),
            )
            conn.commit()
        return todo_id

    def complete(self, todo_id: str) -> bool:
        return self._update_status(todo_id, "done")

    def cancel(self, todo_id: str) -> bool:
        return self._update_status(todo_id, "cancelled")

    def _update_status(self, todo_id: str, status: str) -> bool:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid todo status: {status}")
        completed_at = datetime.now(timezone.utc).isoformat() if status in {"done", "cancelled"} else None
        with self._connect() as conn:
            cursor = conn.execute(
                "UPDATE todos SET status = ?, completed_at = ? WHERE id = ?",
                (status, completed_at, todo_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def remove(self, todo_id: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            return cursor.rowcount > 0

    def list(self, session_id: str) -> List[TodoItem]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, session_id, task, status, created_at, completed_at FROM todos WHERE session_id = ? ORDER BY created_at ASC",
                (session_id,),
            ).fetchall()
        return [self._row_to_item(row) for row in rows]

    def list_all(self) -> List[TodoItem]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, session_id, task, status, created_at, completed_at FROM todos ORDER BY created_at ASC"
            ).fetchall()
        return [self._row_to_item(row) for row in rows]

    def clear_completed(self, session_id: str) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM todos WHERE session_id = ? AND status = ?",
                (session_id, "done"),
            )
            conn.commit()
            return cursor.rowcount

    def stats(self, session_id: str) -> Dict[str, int]:
        items = self.list(session_id)
        return {
            "total": len(items),
            "pending": sum(1 for item in items if item.status == "pending"),
            "done": sum(1 for item in items if item.status == "done"),
            "cancelled": sum(1 for item in items if item.status == "cancelled"),
        }

    def get(self, todo_id: str) -> Optional[TodoItem]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, session_id, task, status, created_at, completed_at FROM todos WHERE id = ?",
                (todo_id,),
            ).fetchone()
        return self._row_to_item(row) if row else None


def todo_symbol(status: str) -> str:
    """Return a display symbol for a todo status."""

    if status == "done":
        return "✓"
    if status == "cancelled":
        return "✗"
    return "□"


def format_todo_item(item: TodoItem) -> str:
    """Render a todo item in a concise human-readable format."""

    return f"{todo_symbol(item.status)} [{item.id}] {item.task}"
