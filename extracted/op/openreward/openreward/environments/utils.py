import asyncio
import inspect
from typing import Any, Callable


async def run_user_callable(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Invoke a user-supplied callback without blocking the event loop.

    The env-server runs on a single uvicorn worker; a sync user callback that
    does I/O (file reads, sync HTTP, subprocess, etc.) would freeze every
    other in-flight request. This helper inspects the callable:

    - ``async def`` → awaited on the event loop.
    - plain sync → executed in a thread via ``asyncio.to_thread`` (which
      ``contextvars.copy_context().run``s under the hood, so structlog's
      request-context bindings survive into the thread).
    - sync function that returns an awaitable (legacy pattern) → sync part
      runs in a thread, awaitable result is awaited on the loop.
    """
    if inspect.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    result = await asyncio.to_thread(fn, *args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    return result
