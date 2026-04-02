"""Async bridge — run sync DB calls off the event loop.

Provides ``run_db()`` which executes a synchronous callable in a dedicated
single-thread executor.  This prevents SQLite I/O (and any lock-retry
``time.sleep`` inside ``_UnclosableConnection._retry``) from blocking the
asyncio event loop that drives the MCP server and scheduler.

The executor uses exactly **one** worker thread so that all DB operations are
serialised, matching SQLite's single-writer constraint and satisfying the
``check_same_thread=False`` contract (only one non-main thread ever touches
the connection).
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import threading
from typing import Any, Callable, TypeVar

T = TypeVar("T")

_db_executor: concurrent.futures.ThreadPoolExecutor | None = None
_lock = threading.Lock()


def _get_executor() -> concurrent.futures.ThreadPoolExecutor:
    """Return (lazily-created) single-thread executor for DB work."""
    global _db_executor
    if _db_executor is None:
        with _lock:
            if _db_executor is None:
                _db_executor = concurrent.futures.ThreadPoolExecutor(
                    max_workers=1,
                    thread_name_prefix="heylead-db",
                )
    return _db_executor


async def run_db(fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Run a sync DB function in the dedicated DB thread.

    Usage::

        result = await run_db(get_setting, "setup_complete", False)
        campaigns = await run_db(list_campaigns, status="active")
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _get_executor(),
        lambda: fn(*args, **kwargs),
    )
