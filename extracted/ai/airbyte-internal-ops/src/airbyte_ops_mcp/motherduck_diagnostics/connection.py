# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MotherDuck admin connection management for diagnostics queries."""

from __future__ import annotations

import contextlib
import os
import threading
from typing import Any

import duckdb

_MOTHERDUCK_ADMIN_TOKEN_ENV = "MOTHERDUCK_ADMIN_TOKEN"

_connection_lock = threading.Lock()
_cached_connection: duckdb.DuckDBPyConnection | None = None


def _get_admin_token() -> str:
    """Retrieve the MotherDuck admin token from environment."""
    token = os.environ.get(_MOTHERDUCK_ADMIN_TOKEN_ENV)
    if not token:
        raise RuntimeError(
            f"Missing {_MOTHERDUCK_ADMIN_TOKEN_ENV} environment variable. "
            "This token must have org admin privileges to access QUERY_HISTORY."
        )
    return token


def _get_or_create_connection() -> duckdb.DuckDBPyConnection:
    """Get or create the cached admin connection (caller must hold `_connection_lock`)."""
    global _cached_connection

    if _cached_connection is not None:
        try:
            _cached_connection.execute("SELECT 1")
            return _cached_connection
        except duckdb.Error:
            with contextlib.suppress(duckdb.Error):
                _cached_connection.close()
            _cached_connection = None

    token = _get_admin_token()
    connection_string = f"md:?motherduck_token={token}"
    conn = duckdb.connect(connection_string)
    _cached_connection = conn
    return conn


def execute_admin_query(
    sql: str, params: list[Any] | None = None
) -> list[dict[str, Any]]:
    """Execute a query on the admin connection and return rows as dicts.

    Thread-safe: holds the connection lock for the entire execute+fetch cycle
    so concurrent callers do not interleave operations on the shared DuckDB
    connection.
    """
    with _connection_lock:
        conn = _get_or_create_connection()
        result = conn.execute(sql, params or [])
        columns = [desc[0] for desc in result.description] if result.description else []
        return [
            dict(zip(columns, row_tuple, strict=False))
            for row_tuple in result.fetchall()
        ]


def close_admin_connection() -> None:
    """Close the cached admin connection if it exists."""
    global _cached_connection

    with _connection_lock:
        if _cached_connection is not None:
            with contextlib.suppress(duckdb.Error):
                _cached_connection.close()
            _cached_connection = None
