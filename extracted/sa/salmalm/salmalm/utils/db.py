"""DB common patterns — initialization and query wrappers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Union

from salmalm.db.connection import get_connection
from salmalm.db.sql_compat import adapt_sql

log = logging.getLogger(__name__)


def connect(
    path: Union[str, Path],
    *,
    wal: bool = True,
    row_factory: bool = False,
    check_same_thread: bool = True,
) -> object:
    """Open a DB connection with common defaults.

    Parameters
    ----------
    path : path to the database file.
    wal : enable WAL journal mode (default True).
    row_factory : keep dict-style rows where backend supports it.
    check_same_thread : kept for backwards-compatibility.
    """
    conn = get_connection(Path(path))
    if row_factory:
        setattr(conn, "row_factory", getattr(conn, "row_factory", None))
    return conn


def ensure_table(conn: object, ddl: str) -> None:
    """Execute a CREATE TABLE IF NOT EXISTS statement."""
    conn.execute(adapt_sql(ddl))
    conn.commit()


def query_all(conn: object, sql: str, params: tuple = ()) -> list:
    """Fetch all rows for a query."""
    return conn.execute(adapt_sql(sql), params).fetchall()


def query_one(conn: object, sql: str, params: tuple = ()) -> Optional[tuple]:
    """Fetch a single row."""
    return conn.execute(adapt_sql(sql), params).fetchone()
