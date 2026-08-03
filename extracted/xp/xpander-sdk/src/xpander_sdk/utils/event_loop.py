"""
Utilities for managing event loop execution in the xpander.ai SDK.

This module provides utilities for handling asyncio event loops, enabling
synchronous execution of coroutines in environments that may not natively
support asynchronous operations.
"""

import asyncio
import concurrent.futures
import contextvars
from typing import Any, Coroutine

# Long-lived so a per-action sync wrapper doesn't pay thread creation every call.
# Threads are reused; each call still gets its own loop.
_RUNNER_POOL = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="xpander-run-sync")


def run_sync(coro: Coroutine[Any, Any, Any]) -> Any:
    """
    Synchronously run a coroutine, including from inside a thread that already
    drives a running event loop (Jupyter, FastAPI / uvicorn request handlers,
    agno tool callables).

    A running loop is never re-entered. Re-entrancy used to be provided by
    ``nest_asyncio``, which patches ``run_forever`` / ``run_until_complete`` /
    ``_run_once`` on the loop class and swaps ``asyncio.Task`` and ``Future``
    process-wide; on a live server that unwinds the host's ``asyncio.run`` and
    kills the process mid-request. The coroutine is handed to a private loop on
    a pooled worker thread instead - the caller blocks, the host loop is
    untouched, and the caller's ``contextvars`` travel with it.

    Prefer awaiting the ``a``-prefixed coroutine directly when the caller is
    already async; this helper exists for the SDK's synchronous API surface.

    Args:
        coro (Coroutine[Any, Any, Any]): The coroutine to be executed. Tasks and
            futures are bound to the loop that created them and cannot be moved.

    Returns:
        Any: The result of the coroutine execution.

    Raises:
        TypeError: If a loop-bound ``Task`` / ``Future`` is passed instead of a
            coroutine object.

    Example:
        >>> async def fetch_data():
        ...     # simulate async operation
        ...     await asyncio.sleep(1)
        ...     return "data"

        >>> result = run_sync(fetch_data())
        >>> print(result)  # Outputs: "data"
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is None or not loop.is_running():
        return asyncio.run(coro)

    if asyncio.isfuture(coro):
        raise TypeError(
            "run_sync() needs a coroutine object (e.g. some_async_fn()); a Task or "
            "Future belongs to the loop that created it and cannot be run on another."
        )

    def _run_in_thread() -> Any:
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coro)
        finally:
            asyncio.set_event_loop(None)
            new_loop.close()

    # Without the copied context the worker thread starts blank, dropping ContextVars
    # such as the current tool call id that downstream requests read for their headers.
    context = contextvars.copy_context()
    return _RUNNER_POOL.submit(context.run, _run_in_thread).result()
