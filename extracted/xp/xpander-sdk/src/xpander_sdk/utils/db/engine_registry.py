"""Process-global SQLAlchemy engine registry for agno Postgres sessions.

agno's ``PostgresDb`` / ``AsyncPostgresDb`` build their own SQLAlchemy engine
when handed a ``db_url``, with default pool settings (no ``pool_pre_ping``, no
``pool_recycle``) and a brand-new engine per instance. In the worker path a db
is constructed per task, so every task pays a cold Neon connect and never reuses
a pool. Worse, naively reusing agno's default engine stalls: Neon is serverless
and drops idle connections, so the next read on a checked-out-but-dead socket
blocks until it times out and reconnects.

This registry hands agno a shared, pre-configured engine instead (via the
``db_engine`` kwarg both classes accept). Engines are keyed by
``(normalized_db_url, async_engine)`` and live for the process lifetime. The
schema is deliberately NOT part of the key: schema is passed to ``PostgresDb``
separately, so one engine per database serves every agent schema.
"""

from __future__ import annotations

import threading
from typing import Dict, Tuple, Union

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# Sized for the worker's concurrency ceiling (up to 4 concurrent executions/pod)
# with a little headroom so a burst doesn't queue on the pool.
POOL_SIZE = 5
MAX_OVERFLOW = 5
POOL_TIMEOUT = 10
# Recycle below Neon's idle-connection cutoff so we never hand out a dead socket.
POOL_RECYCLE = 300

_engines: Dict[Tuple[str, bool], Union[Engine, AsyncEngine]] = {}
_lock = threading.Lock()


def _normalize(db_url: str) -> str:
    return (db_url or "").strip()


def get_or_create_engine(
    db_url: str, *, async_engine: bool
) -> Union[Engine, AsyncEngine]:
    """Return a shared pooled engine for ``db_url``, creating it once per (url, mode).

    ``db_url`` must already carry agno's driver rewrite
    (``postgresql+psycopg`` / ``postgresql+psycopg_async``) so the engine matches
    the connection agno would otherwise build itself.
    """
    key = (_normalize(db_url), bool(async_engine))

    existing = _engines.get(key)
    if existing is not None:
        return existing

    with _lock:
        # Re-check under the lock so a racing caller doesn't build a duplicate.
        existing = _engines.get(key)
        if existing is not None:
            return existing

        kwargs = dict(
            pool_pre_ping=True,
            pool_recycle=POOL_RECYCLE,
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            pool_timeout=POOL_TIMEOUT,
        )
        if async_engine:
            engine: Union[Engine, AsyncEngine] = create_async_engine(key[0], **kwargs)
        else:
            engine = create_engine(key[0], **kwargs)

        _engines[key] = engine
        return engine


def dispose_all() -> None:
    """Dispose every registered engine and clear the registry (clean shutdown)."""
    with _lock:
        engines = list(_engines.values())
        _engines.clear()

    for engine in engines:
        try:
            # AsyncEngine.dispose() is a coroutine; dispose its underlying sync
            # engine instead so shutdown needs no running event loop.
            target = engine.sync_engine if isinstance(engine, AsyncEngine) else engine
            target.dispose()
        except Exception as exc:
            logger.warning(f"Failed to dispose db engine - {exc}")
