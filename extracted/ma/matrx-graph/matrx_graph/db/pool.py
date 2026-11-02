"""Thin wrapper around matrx-orm's AsyncDatabaseManager for code that wants to use
raw asyncpg SQL inside matrx-graph (e.g. PostgresCheckpointer).

matrx-orm owns the connection pool; matrx-graph does not create its own.
The `config_name` defaults to 'supabase_automation_matrix' — the same name
aidream registers in `db/__init__.py`. Host apps with a different main
database name should override via `set_db_config_name()` at startup.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import asyncpg

_DEFAULT_CONFIG_NAME: str = "supabase_automation_matrix"
_CONFIG_NAME: str = _DEFAULT_CONFIG_NAME


def set_db_config_name(name: str) -> None:
    """Override the matrx-orm config_name matrx-graph will acquire from.

    Call once at startup if the host app registered its main DB under a name
    other than 'supabase_automation_matrix'.
    """
    global _CONFIG_NAME
    _CONFIG_NAME = name


def get_db_config_name() -> str:
    return _CONFIG_NAME


@asynccontextmanager
async def acquire(
    timeout: float = 10.0,  # noqa: ASYNC109 — mirrors matrx-orm's get_connection API
) -> AsyncIterator[asyncpg.Connection]:
    """Acquire a connection from the matrx-orm pool.

    Raises a clear RuntimeError if matrx-orm isn't installed — that's a
    deployment / config issue, not a workflow issue, so fail early.
    """
    try:
        from matrx_orm.core.async_db_manager import AsyncDatabaseManager
    except ImportError as e:
        raise RuntimeError(
            "matrx-graph postgres features require `matrx-orm` to be installed "
            "and a database registered via `register_database_from_env()`. "
            "Install with `pip install matrx-graph[postgres]`."
        ) from e

    async with AsyncDatabaseManager.get_connection(_CONFIG_NAME, timeout=timeout) as conn:
        yield conn
