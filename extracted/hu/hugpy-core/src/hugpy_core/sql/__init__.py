"""Core's database: how it is opened. Its tables and views are in create.py.

One file (settings.database()), in WAL mode: the door's readers never wait on the collector's writes. A part that
writes opens its own connection for as long as one piece of work takes."""
from ..imports import (
    connect_wal,
    open_readonly,
    os,
)
from .. import settings
from .create import TABLES, VIEWS


def prepare() -> str:
    """The database with its tables, and its views as this version defines them. Run once, when Core starts (and
    by the system install). Returns the path."""
    path = settings.database()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = connect_wal(path)
    try:
        with conn:
            for statement in TABLES:
                conn.execute(statement)
            for name, select in VIEWS.items():
                conn.execute(f'DROP VIEW IF EXISTS {name}')
                conn.execute(f'CREATE VIEW {name} AS {select}')
    finally:
        conn.close()
    return path


def writer():
    """A connection that writes. `with writer() as conn:` is not used: the caller commits (``with conn:``) and
    closes it."""
    return connect_wal(settings.database())


def reader():
    """A read-only connection (rows by name)."""
    return open_readonly(settings.database())


def rows(sql: str, params=()) -> list:
    """The rows of one read, each a dict."""
    conn = reader()
    try:
        return [dict(row) for row in conn.execute(sql, params)]
    finally:
        conn.close()


__all__ = ['prepare', 'reader', 'rows', 'writer', 'TABLES', 'VIEWS']
