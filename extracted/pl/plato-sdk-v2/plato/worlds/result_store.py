"""Simple sqlite-based result store for caching agent outputs."""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path


class ResultStore:
    """Key-value store backed by sqlite for caching completed work."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS results "
            "(key TEXT PRIMARY KEY, output TEXT, created_at TEXT DEFAULT (datetime('now')))"
        )
        self._conn.commit()

    @staticmethod
    def make_key(*parts: str) -> str:
        """Create a deterministic key by hashing joined parts."""
        return hashlib.sha256("|".join(parts).encode()).hexdigest()

    def has(self, key: str) -> bool:
        cur = self._conn.execute("SELECT 1 FROM results WHERE key = ?", (key,))
        return cur.fetchone() is not None

    def get(self, key: str) -> str | None:
        cur = self._conn.execute("SELECT output FROM results WHERE key = ?", (key,))
        row = cur.fetchone()
        return row[0] if row else None

    def put(self, key: str, output: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO results (key, output) VALUES (?, ?)",
            (key, output),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> ResultStore:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
