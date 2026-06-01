"""
Safe instrumentation utilities.

Provides dont_throw / dont_throw_async decorators and safe_context_run to
guarantee that instrumentation code never propagates exceptions into user
application code.

Inspired by Traceloop's OpenLLMetry safe-wrapper pattern.
"""

from __future__ import annotations

import asyncio
import contextvars
import functools
import logging
import threading
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def dont_throw(func: F) -> F:
    """Sync decorator — swallows all exceptions, returns None on failure.

    On failure a WARNING is logged that includes the module and qualified name
    of the wrapped function together with full traceback context (exc_info=True).
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.warning(
                "Aigie instrumentation error in %s.%s — suppressing to protect user code.",
                func.__module__,
                func.__qualname__,
                exc_info=True,
            )
            return None

    return wrapper  # type: ignore[return-value]


def dont_throw_async(func: F) -> F:
    """Async variant of dont_throw — swallows all exceptions, returns None on failure."""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception:
            logger.warning(
                "Aigie instrumentation error in %s.%s — suppressing to protect user code.",
                func.__module__,
                func.__qualname__,
                exc_info=True,
            )
            return None

    return wrapper  # type: ignore[return-value]


def safe_context_run(coro: Coroutine[Any, Any, Any]) -> Any:
    """Run *coro* while preserving the current contextvars snapshot.

    Two execution paths:

    * **No running event loop** — delegates directly to ``asyncio.run(coro)``.
    * **Inside a running event loop** — spawns a daemon thread carrying a copy
      of the current ``contextvars`` context so that trace IDs and other
      context variables are visible inside the coroutine.  The thread is joined
      with a 30-second timeout.

    Exceptions raised by the coroutine are always re-raised to the caller.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is None:
        # No loop active — simple path.
        return asyncio.run(coro)

    # A loop is already running; we must not call asyncio.run() or
    # loop.run_until_complete() — that would raise RuntimeError.
    # Spawn a thread with a copy of the current context so that all
    # contextvars are accessible inside the coroutine.
    ctx = contextvars.copy_context()
    result_holder: list[Any] = [None]
    exc_holder: list[BaseException | None] = [None]

    def _run() -> None:
        def _inner() -> Any:
            return asyncio.run(coro)

        try:
            result_holder[0] = ctx.run(_inner)
        except BaseException as exc:
            exc_holder[0] = exc

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout=30)

    if exc_holder[0] is not None:
        raise exc_holder[0]

    return result_holder[0]


def schedule_async(coro: Coroutine[Any, Any, Any]) -> Any:
    """Schedule an async coroutine from any context without creating competing event loops.

    * **Loop IS running** — uses ``loop.create_task()`` (cooperative, non-blocking).
    * **No loop** — falls back to ``safe_context_run()`` (thread with own loop).

    This MUST be used instead of bare ``asyncio.run()`` in all SDK hot paths.
    ``asyncio.run()`` creates a new event loop in the caller's thread, which
    competes with any existing loop (e.g., SQS consumer, FastAPI) and causes
    starvation/timeouts.

    Returns the Task (if loop running) or the coroutine result (if no loop),
    or None if scheduling failed.
    """
    try:
        loop = asyncio.get_running_loop()
        return loop.create_task(coro)
    except RuntimeError:
        # No running loop — use thread-based fallback
        try:
            return safe_context_run(coro)
        except Exception:
            logger.warning("schedule_async: failed to schedule coroutine", exc_info=True)
            return None
