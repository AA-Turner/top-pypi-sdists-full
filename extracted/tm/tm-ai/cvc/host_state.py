"""
Host-level persistent state — survives gateway restart, reboot, a year.

This is the SINGLE SOURCE OF TRUTH for the active workspace pointer, the
last-used workspace, and any other machine-global CVC settings.

Why a new SQLite DB instead of the sidecar file `~/.cvc/active_workspace`?
The sidecar was losing writes (the file on Jai's machine contained
`/Users/jkm--` — truncated garbage). A SQLite DB with WAL gives us:
  * Atomic writes (no torn values)
  * Survives concurrent reads from gateway + dashboard
  * Crash-safe via journal
  * Survives file truncation / partial writes

The legacy sidecar file (`~/.cvc/active_workspace`) is read once on first
boot and migrated into the DB. After that it's ignored.

Schema is intentionally tiny — just a key/value table. Add columns to
``HostState`` as new global settings appear.
"""

from __future__ import annotations

import logging
import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)

# Host-level paths
HOST_DIR = Path.home() / ".cvc"
HOST_DB_PATH = HOST_DIR / "host_state.db"
LEGACY_SIDECAR = HOST_DIR / "active_workspace"

# KV keys
KV_ACTIVE_WORKSPACE = "active_workspace_path"
KV_LAST_ACCESS = "active_workspace_last_access"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS kv (
    key         TEXT PRIMARY KEY,
    value       TEXT NOT NULL,
    updated_at  REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS kv_history (
    key         TEXT NOT NULL,
    value       TEXT NOT NULL,
    updated_at  REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_kv_history_key_time
    ON kv_history(key, updated_at DESC);
"""


class HostState:
    """Thread-safe persistent key/value store at the host level.

    Lives at ``~/.cvc/host_state.db``. Survives everything.
    """

    def __init__(self, db_path: Path | str | None = None) -> None:
        self._db_path = Path(db_path) if db_path is not None else HOST_DB_PATH
        self._lock = threading.RLock()
        self._conn = self._open_or_recover(self._db_path)

    def _open_or_recover(self, path: Path) -> sqlite3.Connection:
        """Open the DB at ``path``. If the file is corrupt or unreadable,
        quarantine it and start a fresh DB — never raise during boot."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(
                str(path),
                check_same_thread=False,
                isolation_level=None,
            )
            conn.row_factory = sqlite3.Row
            conn.executescript(_SCHEMA)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            cur = conn.execute(
                "SELECT value FROM kv WHERE key = 'schema_version'"
            ).fetchone()
            if cur is None:
                conn.execute(
                    "INSERT INTO kv(key, value, updated_at) VALUES (?, ?, ?)",
                    ("schema_version", "1", time.time()),
                )
            return conn
        except sqlite3.DatabaseError as exc:
            # Quarantine the corrupt file and start fresh. The sidecar
            # migration in get_active_workspace() will repopulate from
            # the sidecar.
            logger.error(
                "HostState DB at %s is corrupt (%s) — quarantining and "
                "starting fresh; legacy sidecar will be used as fallback",
                path, exc,
            )
            try:
                quarantine = path.with_suffix(
                    f".corrupt-{int(time.time())}.bak"
                )
                path.replace(quarantine)
            except OSError:
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
            # Retry once
            path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(
                str(path),
                check_same_thread=False,
                isolation_level=None,
            )
            conn.row_factory = sqlite3.Row
            conn.executescript(_SCHEMA)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute(
                "INSERT INTO kv(key, value, updated_at) VALUES (?, ?, ?)",
                ("schema_version", "1", time.time()),
            )
            return conn

    # ── KV primitives ────────────────────────────────────────────────
    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                yield self._conn
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    def get(self, key: str, default: str | None = None) -> str | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT value FROM kv WHERE key = ?", (key,)
            ).fetchone()
            return row["value"] if row else default

    def set(self, key: str, value: str) -> None:
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO kv(key, value, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value, "
                "updated_at = excluded.updated_at",
                (key, value, time.time()),
            )
            conn.execute(
                "INSERT INTO kv_history(key, value, updated_at) VALUES (?, ?, ?)",
                (key, value, time.time()),
            )

    def delete(self, key: str) -> None:
        with self._tx() as conn:
            conn.execute("DELETE FROM kv WHERE key = ?", (key,))

    def history(self, key: str, limit: int = 10) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT value, updated_at FROM kv_history "
                "WHERE key = ? ORDER BY updated_at DESC LIMIT ?",
                (key, limit),
            ).fetchall()
            return [{"value": r["value"], "updated_at": r["updated_at"]} for r in rows]

    # ── Active workspace: the high-level API ──────────────────────────
    def get_active_workspace(self) -> Path | None:
        """Return the persisted active workspace path, validating it exists.

        Falls back to the legacy sidecar file on first call (one-shot
        migration). Returns None if nothing valid is recorded.
        """
        raw = self.get(KV_ACTIVE_WORKSPACE)
        if raw is None and LEGACY_SIDECAR.exists():
            # One-shot migration of the legacy sidecar.
            try:
                raw = LEGACY_SIDECAR.read_text(encoding="utf-8").strip()
                if raw:
                    logger.info("Migrating legacy active_workspace sidecar: %r", raw)
                    self.set(KV_ACTIVE_WORKSPACE, raw)
                    # Don't delete the sidecar — keep it as a redundant backup.
            except OSError as exc:
                logger.warning("Could not read legacy sidecar: %s", exc)
                raw = None
        if not raw:
            return None
        try:
            p = Path(os.path.expanduser(raw))
        except (TypeError, ValueError):
            logger.warning("Persisted active workspace is not a valid path: %r", raw)
            return None
        if not p.is_dir():
            logger.warning(
                "Persisted active workspace no longer exists on disk: %s "
                "(keeping pointer for diagnostics — run `cvc workspace reset` "
                "if you want to clear it)",
                p,
            )
            return None
        return p

    def set_active_workspace(self, path: Path) -> None:
        """Persist the active workspace path. Always writes BOTH the DB
        (source of truth) AND the legacy sidecar (redundant backup).

        Never raises — host-state writes must not crash the gateway.
        """
        path_str = str(path)
        try:
            self.set(KV_ACTIVE_WORKSPACE, path_str)
            self.set(KV_LAST_ACCESS, str(time.time()))
        except sqlite3.DatabaseError as exc:
            # If the DB itself is corrupt, fall back to the sidecar.
            logger.error("HostState DB write failed: %s — writing sidecar only", exc)
        try:
            LEGACY_SIDECAR.parent.mkdir(parents=True, exist_ok=True)
            # Write atomically: tmp + rename, so a crash mid-write doesn't
            # leave a half-written file.
            tmp = LEGACY_SIDECAR.with_suffix(".tmp")
            tmp.write_text(path_str, encoding="utf-8")
            tmp.replace(LEGACY_SIDECAR)
        except OSError as exc:
            logger.warning("Could not update legacy sidecar: %s", exc)

    def clear_active_workspace(self) -> None:
        """Forget the persisted active workspace."""
        try:
            self.delete(KV_ACTIVE_WORKSPACE)
        except sqlite3.DatabaseError:
            pass
        try:
            LEGACY_SIDECAR.unlink(missing_ok=True)
        except OSError:
            pass


# ── Singleton (lazy, thread-safe) ────────────────────────────────────
_singleton: HostState | None = None
_singleton_lock = threading.Lock()


def get_host_state() -> HostState:
    """Return the process-wide HostState instance."""
    global _singleton
    if _singleton is None:
        with _singleton_lock:
            if _singleton is None:
                _singleton = HostState()
    return _singleton


def reset_singleton_for_tests() -> None:
    """Drop the process-wide singleton. Tests use this to isolate state
    between cases without leaking the prior DB path into the next one.
    """
    global _singleton
    with _singleton_lock:
        if _singleton is not None:
            try:
                _singleton._conn.close()
            except Exception:
                pass
        _singleton = None


# ── Convenience helpers ──────────────────────────────────────────────
def load_active_workspace() -> Path | None:
    """Module-level wrapper. Equivalent to WorkspaceManager.load_active_workspace
    but reads from the durable DB instead of the sidecar file.
    """
    return get_host_state().get_active_workspace()


def save_active_workspace(path: Path) -> None:
    """Module-level wrapper. Writes both DB and sidecar."""
    get_host_state().set_active_workspace(path)