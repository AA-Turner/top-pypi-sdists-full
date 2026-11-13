"""Lifted verbatim from fitevict/observability/store.py (sha256 95e49afe9efd50c3): Store and what they reach in that file.
Written by tools/refactors/core-off-fitevict-20261110/lift.py; the definitions below are the original text."""
from __future__ import annotations

import logging
import os
import re
import sqlite3
import threading
import time
import urllib.parse
from contextlib import contextmanager
from importlib import resources
from typing import Any, Callable, Iterator, List, Optional, Sequence

from hugpy_resources.imports.classes.errors import StoreError
from hugpy_resources.imports.functions.sqlite_callbacks import _register, _statements

log = logging.getLogger("hugpy_core.store")
_MIGRATION_RE = re.compile(r'^(\d{4})_[a-z0-9_]+\.sql$')            # imports.constants.observability.STORE_MIGRATION_RE
MODES = {'private': (448, 384, 384), 'group': (488, 416, 432)}      # ...STORE_MODES: directory, files, -shm
_owned_C_STORE_BUSY_TIMEOUT_MS = 10000                              # imports.constants.storage


class Store:
    """One SQLite store: where it lives, which migrations shape it, how it is shared."""

    def __init__(self, home: Callable[[], str], migrations_package: str, filename: str,
                 mode_env: Optional[str] = None, database_env: Optional[str] = None):
        self._home = home
        self.migrations_package = migrations_package
        self.filename = filename
        self.mode_env = mode_env
        self.database_env = database_env
        self._lock = threading.RLock()
        self._conn: Optional[sqlite3.Connection] = None
        self._path: Optional[str] = None
        self._pid: Optional[int] = None
        self._listeners: List[Callable[[], None]] = []
        self._changed = threading.Condition()
        self.changes = 0

    # location / sharing
    def home(self) -> str:
        return self._home()

    def database_url(self) -> str:
        value = (os.environ.get(self.database_env, '') if self.database_env else '').strip()
        if not value and self.database_env == "HUGPY_WRAPPER_DATABASE_URL":
            # Explicit configuration remains authoritative.  Only the module's
            # default Wrapper store participates in local abstract-database
            # discovery; ad-hoc Store instances keep their requested location.
            try:
                from .database_discovery import database_url as discovered_database_url
                value = discovered_database_url()
            except Exception:  # noqa: BLE001 - discovery must never block startup
                value = ''
        if value and not value.startswith(('sqlite:///', 'postgresql://', 'postgres://')):
            raise StoreError('database URL must use sqlite:/// or postgresql://')
        return value

    def backend(self) -> str:
        return 'postgresql' if self.database_url().startswith(('postgresql://', 'postgres://')) else 'sqlite'

    def path(self) -> Optional[str]:
        value = self.database_url()
        if self.backend() == 'postgresql':
            return None
        if value:
            parts = urllib.parse.urlsplit(value)
            if parts.netloc or parts.query or parts.fragment:
                raise StoreError('SQLite database URL cannot include a host, query, or fragment')
            path = urllib.parse.unquote(value[len('sqlite:///'):])
            if not path or path == ':memory:':
                raise StoreError('Wrapper requires a persistent SQLite file')
            return os.path.abspath(os.path.expanduser(path))
        return os.path.join(self.home(), self.filename)

    def modes(self) -> tuple:
        mode = (os.environ.get(self.mode_env, "") if self.mode_env else "").strip().lower() or "private"
        return MODES.get(mode, MODES["private"])

    def _prepare_dir(self, d: str) -> None:
        dmode = self.modes()[0]
        os.makedirs(d, mode=dmode, exist_ok=True)
        try:
            os.chmod(d, dmode)
        except OSError:
            pass                                   # not ours to change (e.g. a shared FITEVICT_HOME)

    def _set_file_modes(self, p: str) -> None:
        _d, fmode, shm = self.modes()
        for suffix, m in (("", fmode), ("-wal", fmode), ("-shm", shm)):
            try:
                os.chmod(p + suffix, m)
            except OSError:
                pass

    # migrations
    def migrations(self) -> list:
        """[(version, name, sql)] shipped with the package, in order."""
        out = []
        for entry in resources.files(self.migrations_package).joinpath("schema").iterdir():
            m = _MIGRATION_RE.match(entry.name)
            if m:
                out.append((int(m.group(1)), entry.name, entry.read_text(encoding="utf-8")))
        return sorted(out)

    def _migrate(self, conn: sqlite3.Connection) -> int:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        for ver, name, sql in self.migrations():
            if ver <= version:
                continue
            conn.execute("BEGIN IMMEDIATE")    # another process may be migrating: wait, then re-check
            try:
                if conn.execute("PRAGMA user_version").fetchone()[0] >= ver:
                    conn.execute("COMMIT")
                    continue
                for stmt in _statements(sql):
                    conn.execute(stmt)
                conn.execute(f"PRAGMA user_version = {int(ver)}")
                conn.execute("COMMIT")
            except Exception as exc:
                conn.execute("ROLLBACK")
                raise StoreError(f"migration {name} failed: {exc}") from exc
            version = ver
            log.info("store: applied migration %s", name)
        return version

    # open / integrity
    @staticmethod
    def _connect(p: str) -> sqlite3.Connection:
        conn = sqlite3.connect(p, timeout=_owned_C_STORE_BUSY_TIMEOUT_MS / 1000, check_same_thread=False,
                               isolation_level=None)
        conn.row_factory = sqlite3.Row
        _register(conn)
        conn.execute(f"PRAGMA busy_timeout = {int(_owned_C_STORE_BUSY_TIMEOUT_MS)}")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        return conn

    @staticmethod
    def _healthy(conn: sqlite3.Connection) -> bool:
        row = conn.execute("PRAGMA quick_check").fetchone()
        return bool(row) and row[0] == "ok"

    @staticmethod
    def _corrupt_error(exc: sqlite3.DatabaseError) -> bool:
        code = getattr(exc, "sqlite_errorcode", None)
        if code is not None:
            return (code & 0xff) in (sqlite3.SQLITE_CORRUPT, sqlite3.SQLITE_NOTADB)
        message = str(exc).lower()
        return "database disk image is malformed" in message or "file is not a database" in message

    @staticmethod
    def _quarantine(p: str) -> None:
        stamp = time.strftime("%Y%m%dT%H%M%S")
        for suffix in ("", "-wal", "-shm"):
            if os.path.exists(p + suffix):
                os.replace(p + suffix, f"{p}.corrupt-{stamp}{suffix}")
        log.warning("store: %s failed its integrity check; moved aside as %s.corrupt-%s and recreated",
                    p, p, stamp)

    def _open(self):
        if self.backend() == 'postgresql':
            if max(v for v, _name, _sql in self.migrations()) != 32:
                raise StoreError('PostgreSQL migrations must be updated for this Wrapper schema version')
            from .postgres import Connection
            try:
                return Connection(self.database_url(), os.environ.get('HUGPY_WRAPPER_DATABASE_SCHEMA', 'hugpy_wrapper'))
            except Exception as exc:
                raise StoreError('PostgreSQL store unavailable; check the database URL, driver and database permissions') from exc
        p = self.path()
        self._prepare_dir(os.path.dirname(p))
        conn = None
        try:
            conn = self._connect(p)
            ok = self._healthy(conn)
        except sqlite3.DatabaseError as exc:
            if conn is not None:
                conn.close()
                conn = None
            if not self._corrupt_error(exc):
                raise StoreError(f"store open or integrity check failed: {exc}") from exc
            ok = False
        if not ok:
            if conn is not None:
                conn.close()
            self._quarantine(p)
            conn = self._connect(p)
        self._migrate(conn)
        if self.migrations_package == "fitevict.observability":
            self._install_history(conn)
        self._set_file_modes(p)
        return conn

    @staticmethod
    def _install_history(conn: sqlite3.Connection) -> None:
        """(Re)install record_history triggers so no write path loses a prior row."""
        from .record_history import install
        conn.execute("BEGIN IMMEDIATE")
        try:
            install(conn)
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        conn.execute("COMMIT")

    def conn(self) -> sqlite3.Connection:
        """The process-wide connection, opened (and migrated) on first use."""
        with self._lock:
            p = ((self.database_url(), os.environ.get('HUGPY_WRAPPER_DATABASE_SCHEMA', 'hugpy_wrapper'))
                 if self.backend() == 'postgresql' else self.path())
            if self._conn is None or self._pid != os.getpid() or self._path != p or getattr(self._conn, "failed", False):
                if self._conn is not None and self._pid == os.getpid():
                    self._conn.close()
                self._conn, self._path, self._pid = self._open(), p, os.getpid()
            return self._conn

    def close(self) -> None:
        with self._lock:
            if self._conn is not None and self._pid == os.getpid():
                self._conn.close()
            self._conn = self._path = self._pid = None

    # change tracking
    def add_write_listener(self, fn: Callable[[], None]) -> None:
        with self._lock:
            if fn not in self._listeners:
                self._listeners.append(fn)

    def _wrote(self) -> None:
        with self._changed:
            self.changes += 1
            self._changed.notify_all()
        for fn in list(self._listeners):
            try:
                fn()
            except Exception:  # noqa: BLE001 — a listener never breaks a write
                log.exception("store: write listener failed")

    def wait_change(self, since: int, timeout: float) -> int:
        """Block until the change counter passes ``since`` or ``timeout`` runs
        out; returns the counter (long-poll readers resend it next time)."""
        deadline = time.monotonic() + max(0.0, float(timeout))
        with self._changed:
            while self.changes <= since:
                left = deadline - time.monotonic()
                if left <= 0:
                    break
                self._changed.wait(left)
            return self.changes

    # reads / writes
    def read(self, sql: str, params: Sequence[Any] = ()) -> List[sqlite3.Row]:
        with self._lock:
            return self.conn().execute(sql, tuple(params)).fetchall()

    def read_one(self, sql: str, params: Sequence[Any] = ()) -> Optional[sqlite3.Row]:
        rows = self.read(sql, params)
        return rows[0] if rows else None

    def write(self, sql: str, params: Sequence[Any] = ()) -> List[sqlite3.Row]:
        """One statement, atomic on its own; returns RETURNING rows if any."""
        with self._lock:
            conn = self.conn()
            before = conn.total_changes
            rows = conn.execute(sql, tuple(params)).fetchall()
            changed = conn.total_changes != before
        if changed:
            self._wrote()
        return rows

    def write_many(self, sql: str, seq: Sequence[Sequence[Any]]) -> None:
        with self.transaction() as c:
            c.executemany(sql, [tuple(p) for p in seq])

    @contextmanager
    def snapshot(self):
        """A coherent multi-table read, without a writer reservation or notification.

        Like transaction(), this context is not nested. Reads through this Store
        share the same connection and reentrant lock for its duration.
        """
        with self._lock:
            c = self.conn()
            c.execute('BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY'
                      if self.backend() == 'postgresql' else 'BEGIN')
            try:
                yield c
            except BaseException:
                try:
                    c.execute('ROLLBACK')
                except Exception:
                    pass
                raise
            c.execute('COMMIT')

    @contextmanager
    def transaction(self, notify: bool = True) -> Iterator[sqlite3.Connection]:
        """Several statements as one unit (BEGIN IMMEDIATE … COMMIT / ROLLBACK).
        ``notify=False`` = a SENSOR reading (the card's bytes, the host's free
        memory, a serving resident's live bytes): stored, but it moves neither the
        change counter nor the listeners — long-poll readers wake on EVENTS only
        (operator 2026-10-14: no heartbeats)."""
        with self._lock:
            c = self.conn()
            before = c.total_changes
            c.execute("BEGIN IMMEDIATE")
            try:
                yield c
            except BaseException:
                try:
                    c.execute("ROLLBACK")
                except Exception:
                    pass  # disconnected PostgreSQL cannot roll back; preserve the original failure
                raise
            c.execute("COMMIT")
            changed = c.total_changes != before
        if notify and changed:
            self._wrote()
