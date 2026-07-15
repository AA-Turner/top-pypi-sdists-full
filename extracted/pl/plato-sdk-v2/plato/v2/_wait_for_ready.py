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

from plato._generated.models import JobStatus, Status5

DEFAULT_POLL_SECONDS = 300
# Small fixed sleep between polls when the backend returns ``ready=False``.
# Guards against hot-loops if a long-poll ever returns instantly without the
# job being ready; in the normal long-poll case the backend already held the
# connection for ``per_call`` seconds before returning.
_INTER_POLL_SLEEP_SECONDS = 1.0

# Status values that mean the job/session will never become ready. Once one of
# these is observed, polling exits immediately instead of waiting out the
# budget. Sessions only ever expose ``failed`` at the aggregate level; jobs
# additionally expose ``cancelled``/``timeout``/``completed``.
_TERMINAL_JOB_STATUSES: frozenset[JobStatus] = frozenset(
    {JobStatus.failed, JobStatus.cancelled, JobStatus.timeout, JobStatus.completed}
)
_TERMINAL_SESSION_STATUSES: frozenset[Status5] = frozenset({Status5.failed})


class _ReadyResponse(Protocol):
    @property
    def ready(self) -> bool: ...

    @property
    def status(self) -> JobStatus | Status5 | None: ...


T = TypeVar("T", bound=_ReadyResponse)


def _per_call_timeout(deadline: float, poll_seconds: int) -> int:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return 1
    return max(1, min(poll_seconds, int(remaining)))


def is_terminal_status(response: _ReadyResponse) -> bool:
    """Return True if ``response.status`` indicates a no-retry terminal state.

    A terminal status means the job/session will not become ready, so callers
    should surface a permanent-failure error rather than a timeout.
    """
    status = response.status
    if status is None:
        return False
    if isinstance(status, JobStatus):
        return status in _TERMINAL_JOB_STATUSES
    return status in _TERMINAL_SESSION_STATUSES


class JobTerminalStatusError(RuntimeError):
    """Raised when ``wait_for_ready`` reports a terminal status before ``ready=True``.

    Subclasses :class:`RuntimeError` so existing ``except RuntimeError`` handlers
    keep working. Callers that want to retry on the *transient* case (e.g. a
    crashed VM that a fresh ``add_env`` could replace) can catch this type
    specifically without retrying on hard backend errors like an invalid request.

    Attributes:
        job_id: The job/session id that reached a terminal status, or ``None`` for
            session-level wait_for_ready failures that don't carry a job id.
        status: The terminal status value reported by the backend.
        backend_error: The error string the backend attached to the response, if any.
    """

    def __init__(
        self,
        message: str,
        *,
        job_id: str | None,
        status: str,
        backend_error: str | None,
    ) -> None:
        super().__init__(message)
        self.job_id = job_id
        self.status = status
        self.backend_error = backend_error


def poll_until_ready_sync(
    call: Callable[[int], T],
    *,
    timeout: float,
    poll_seconds: int = DEFAULT_POLL_SECONDS,
) -> T:
    """Poll ``call(per_call_timeout)`` until ``ready=True`` or budget exhausted.

    ``call`` receives the per-call long-poll timeout in seconds and returns a
    response with a ``ready: bool`` attribute. The final response is returned
    when ``ready=True``, when ``status`` is in the terminal set, or when the
    total budget is exhausted; callers inspect ``.ready`` / ``.status``.
    """
    deadline = time.monotonic() + timeout
    while True:
        response = call(_per_call_timeout(deadline, poll_seconds))
        if response.ready or is_terminal_status(response):
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
        if response.ready or is_terminal_status(response):
            return response
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return response
        if remaining > _INTER_POLL_SLEEP_SECONDS:
            await asyncio.sleep(_INTER_POLL_SLEEP_SECONDS)
