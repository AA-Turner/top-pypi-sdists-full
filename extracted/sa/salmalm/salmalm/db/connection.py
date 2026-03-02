"""Database connection — PostgreSQL (production) or SQLite (development/test)."""
from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional

DATABASE_URL = os.environ.get("SALMALM_DATABASE_URL", "postgresql://localhost/salmalm")
_URL_IS_PG = bool(DATABASE_URL and DATABASE_URL.lower().startswith("postgresql"))
_USE_PG = False
_pool: Any = None

try:
    if _URL_IS_PG:
        import psycopg2  # type: ignore
        import psycopg2.pool  # type: ignore
        from psycopg2.extras import DictCursor  # type: ignore

        _pool = psycopg2.pool.ThreadedConnectionPool(2, 20, DATABASE_URL)
        _USE_PG = True
except Exception:
    _USE_PG = False
    _pool = None

if _USE_PG:
    OperationalError = psycopg2.OperationalError
    IntegrityError = psycopg2.IntegrityError
    PLACEHOLDER = "%s"
else:
    import sqlite3

    OperationalError = sqlite3.OperationalError
    IntegrityError = sqlite3.IntegrityError
    PLACEHOLDER = "?"
    _lock = threading.Lock()


class _CursorProxy:
    """Cursor proxy that adapts SQLite-ish SQL for PostgreSQL on execute."""

    def __init__(self, cursor: Any):
        self._cursor = cursor

    def execute(self, sql: str, params: Optional[Any] = None) -> "_CursorProxy":
        from salmalm.db.sql_compat import q

        adapted_sql, adapted_params = q(sql, params)
        if adapted_params is None:
            self._cursor.execute(adapted_sql)
        else:
            self._cursor.execute(adapted_sql, adapted_params)
        return self

    def executemany(self, sql: str, param_seq: Any) -> "_CursorProxy":
        from salmalm.db.sql_compat import adapt_sql

        self._cursor.executemany(adapt_sql(sql), param_seq)
        return self

    def __iter__(self):
        return iter(self._cursor)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._cursor, name)


class _PgConnectionProxy:
    """Pooled PostgreSQL connection with sqlite-like convenience methods."""

    def __init__(self, conn: Any):
        self._conn = conn
        self._released = False
        self._row_factory = None
        self.autocommit = False

    @property
    def row_factory(self) -> Any:
        return self._row_factory

    @row_factory.setter
    def row_factory(self, value: Any) -> None:
        self._row_factory = value

    def cursor(self) -> _CursorProxy:
        return _CursorProxy(self._conn.cursor(cursor_factory=DictCursor))

    def execute(self, sql: str, params: Optional[Any] = None) -> _CursorProxy:
        return self.cursor().execute(sql, params)

    def executemany(self, sql: str, param_seq: Any) -> _CursorProxy:
        return self.cursor().executemany(sql, param_seq)

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def close(self) -> None:
        if not self._released:
            release_connection(self)
            self._released = True

    def __enter__(self) -> "_PgConnectionProxy":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.close()
        return False


def get_connection(db_path: str | Path | None = None, *, timeout: float = 30.0, **kwargs) -> Any:
    """Get a database connection for the active backend."""
    if _USE_PG:
        conn = _pool.getconn()
        conn.autocommit = False
        return _PgConnectionProxy(conn)

    path = str(db_path) if db_path else ":memory:"
    conn = sqlite3.connect(path, timeout=timeout, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=10000")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def release_connection(conn: Any) -> None:
    """Release a pooled PostgreSQL connection."""
    if not _USE_PG or _pool is None:
        return
    raw_conn = conn._conn if hasattr(conn, "_conn") else conn
    _pool.putconn(raw_conn)


@contextmanager
def db_conn(db_path: str | Path | None = None, **kwargs):
    """Context manager with commit/rollback lifecycle."""
    conn = get_connection(db_path=db_path, **kwargs)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        if _USE_PG:
            release_connection(conn)
        else:
            conn.close()
