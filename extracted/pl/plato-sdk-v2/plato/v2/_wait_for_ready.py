"""Shared polling loop for ``*.wait_for_ready`` long-poll endpoints.

The backend ``wait_for_ready`` endpoints (``jobs``, ``sessions``) are designed
to be called repeatedly with a short per-call timeout. Passing a large
caller-supplied total budget straight into a single call leaves the underlying
``httpx.AsyncClient`` to time out at its default read timeout (typically 600s)
long before the backend would have returned, surfacing as
``httpx.ReadTimeout`` instead of ``TimeoutError``.

The helpers here loop the call with a short per-call budget (default 10s) and
exit on ``ready=True`` or total-budget exhaustion. Callers receive the final
response and decide what to do with ``ready=False``.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Protocol, TypeVar

DEFAULT_POLL_SECONDS = 300
# Small fixed sleep between polls when the backend returns ``ready=False``.
# Guards against hot-loops if a long-poll ever returns instantly without the
# job being ready; in the normal long-poll case the backend already held the
# connection for ``per_call`` seconds before returning.
_INTER_POLL_SLEEP_SECONDS = 1.0


class _ReadyResponse(Protocol):
    @property
    def ready(self) -> bool: ...


T = TypeVar("T", bound=_ReadyResponse)


def _per_call_timeout(deadline: float, poll_seconds: int) -> int:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return 1
    return max(1, min(poll_seconds, int(remaining)))


def poll_until_ready_sync(
    call: Callable[[int], T],
    *,
    timeout: float,
    poll_seconds: int = DEFAULT_POLL_SECONDS,
) -> T:
    """Poll ``call(per_call_timeout)`` until ``ready=True`` or budget exhausted.

    ``call`` receives the per-call long-poll timeout in seconds and returns a
    response with a ``ready: bool`` attribute. The final response is returned
    regardless of readiness; callers check ``.ready`` themselves.
    """
    deadline = time.monotonic() + timeout
    while True:
        response = call(_per_call_timeout(deadline, poll_seconds))
        if response.ready:
            return response
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return response
        if remaining > _INTER_POLL_SLEEP_SECONDS:
            time.sleep(_INTER_POLL_SLEEP_SECONDS)


async def poll_until_ready_async(
    call: Callable[[int], Awaitable[T]],
    *,
    timeout: float,
    poll_seconds: int = DEFAULT_POLL_SECONDS,
) -> T:
    """Async variant of :func:`poll_until_ready_sync`."""
    deadline = time.monotonic() + timeout
    while True:
        response = await call(_per_call_timeout(deadline, poll_seconds))
        if response.ready:
            return response
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return response
        if remaining > _INTER_POLL_SLEEP_SECONDS:
            await asyncio.sleep(_INTER_POLL_SLEEP_SECONDS)
