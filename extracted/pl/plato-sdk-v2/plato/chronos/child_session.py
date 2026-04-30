"""Heartbeat-aware wait loop for child Chronos sessions.

Worlds that launch child worlds (e.g. CUA benchmark sessions) need more than
``wait_until_complete``: they want heartbeat logs, a constructed session URL,
and the raw ``SessionResponse`` passed through so the world can map it into
its own result schema.

Timeouts are the caller's concern — wrap in :func:`asyncio.wait_for` if you
want a ceiling. The SDK keeps polling until Chronos reports a terminal
status.

Status polls and detail fetches retry transparently on transient HTTP / network
errors (5xx responses, connection resets, timeouts). A single bad poll —
typically an ALB→target connection blip returning 502 with no application-level
error — is otherwise enough to fail an entire long-running parent session.
"""

from __future__ import annotations

import asyncio
import logging
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from time import monotonic
from typing import TYPE_CHECKING, TypeVar

import httpx

from plato.chronos.errors import APIError
from plato.chronos.models import SessionResponse

if TYPE_CHECKING:
    from plato.chronos.sdk import AsyncChronosSession

logger = logging.getLogger(__name__)

_TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled", "error"})

# Status codes that indicate a transient upstream / gateway issue worth
# retrying. 502/504 typically come from ALB or other reverse proxies when the
# upstream connection failed mid-flight; 503 / 500 from the app itself when
# briefly unavailable.
_TRANSIENT_STATUS_CODES = frozenset({500, 502, 503, 504})

DEFAULT_TRANSIENT_MAX_ATTEMPTS = 5
DEFAULT_TRANSIENT_BACKOFF_BASE = 0.5
DEFAULT_TRANSIENT_BACKOFF_CAP = 8.0

T = TypeVar("T")


def _status_str(status: object) -> str:
    value = getattr(status, "value", None)
    return value if isinstance(value, str) else str(status)


def _is_transient_error(exc: BaseException) -> bool:
    """True if ``exc`` looks like a transient gateway / network blip."""
    if isinstance(exc, APIError):
        return exc.status_code in _TRANSIENT_STATUS_CODES
    # httpx.TransportError covers TimeoutException, NetworkError (ConnectError /
    # ReadError / WriteError / CloseError), ProtocolError (RemoteProtocolError),
    # ProxyError, and UnsupportedProtocol.
    return isinstance(exc, httpx.TransportError)


def _backoff_delay(
    attempt: int,
    *,
    base: float,
    cap: float,
) -> float:
    """Exponential backoff with jitter. ``attempt`` is 1-based."""
    deterministic = min(cap, base * (2 ** (attempt - 1)))
    # Equal jitter — half deterministic, half random — keeps polls from
    # synchronizing across many parallel waiters during a shared blip.
    return deterministic / 2 + random.random() * (deterministic / 2)


async def _call_with_transient_retry(
    operation: Callable[[], Awaitable[T]],
    *,
    op_name: str,
    session_id: str | None,
    max_attempts: int,
    backoff_base: float,
    backoff_cap: float,
    log_extra: dict[str, object] | None,
) -> T:
    """Call ``operation`` with retries on transient HTTP / network errors.

    Re-raises the last exception verbatim once ``max_attempts`` is exhausted,
    so callers see the original ``APIError`` / ``httpx.TransportError`` and
    can act on it. Non-transient errors (4xx, programming bugs) are raised
    immediately without retry.
    """
    if max_attempts < 1:
        raise ValueError(f"max_attempts must be >= 1, got {max_attempts}")

    extras_base: dict[str, object] = {
        **(log_extra or {}),
        "session_id": session_id,
        "operation": op_name,
    }

    for attempt in range(1, max_attempts + 1):
        try:
            return await operation()
        except Exception as exc:  # noqa: BLE001 — re-raised below
            if not _is_transient_error(exc):
                raise
            if attempt >= max_attempts:
                logger.error(
                    "Transient error on %s for session=%s after %d attempts; giving up: %s",
                    op_name,
                    session_id,
                    attempt,
                    exc,
                    extra={
                        **extras_base,
                        "attempt": attempt,
                        "max_attempts": max_attempts,
                        "error_type": type(exc).__name__,
                        "status_code": getattr(exc, "status_code", None),
                        "exhausted": True,
                    },
                )
                raise
            sleep_seconds = _backoff_delay(attempt, base=backoff_base, cap=backoff_cap)
            logger.warning(
                "Transient error on %s for session=%s (attempt %d/%d): %s; retrying in %.2fs",
                op_name,
                session_id,
                attempt,
                max_attempts,
                exc,
                sleep_seconds,
                extra={
                    **extras_base,
                    "attempt": attempt,
                    "max_attempts": max_attempts,
                    "sleep_seconds": sleep_seconds,
                    "error_type": type(exc).__name__,
                    "status_code": getattr(exc, "status_code", None),
                    "exhausted": False,
                },
            )
            await asyncio.sleep(sleep_seconds)

    # Unreachable: loop above either returns or raises.
    raise RuntimeError("retry loop exited without returning or raising")


@dataclass
class ChildSessionOutcome:
    """Normalized outcome of a child-session wait.

    ``status`` is one of ``"completed"``, ``"failed"``, ``"cancelled"``, or
    ``"error"`` — whatever Chronos reported. ``details`` is the raw
    :class:`SessionResponse` passed through unchanged so callers can map it
    into their own world-specific result schema.
    """

    status: str
    session_id: str | None = None
    plato_session_id: str | None = None
    session_url: str | None = None
    error: str | None = None
    details: SessionResponse | None = None


async def wait_for_child_session(
    session: AsyncChronosSession,
    *,
    poll_interval: float = 10.0,
    heartbeat_interval: float = 60.0,
    stage_label: str = "child",
    chronos_base_url: str | None = None,
    log_extra: dict[str, object] | None = None,
    message_suffix: str = "",
    transient_max_attempts: int = DEFAULT_TRANSIENT_MAX_ATTEMPTS,
    transient_backoff_base: float = DEFAULT_TRANSIENT_BACKOFF_BASE,
    transient_backoff_cap: float = DEFAULT_TRANSIENT_BACKOFF_CAP,
) -> ChildSessionOutcome:
    """Wait for a Chronos child session to reach a terminal status.

    Polls ``session.get_status`` until the session reports a terminal status,
    then fetches ``session.get_details``. Heartbeat logs are emitted every
    ``heartbeat_interval`` seconds via ``plato.chronos.child_session`` at
    DEBUG level (so Chronos marks them ``plato.debug=True`` and hides them in
    the default trace view, and stderr stays quiet during long waits).

    Both ``get_status`` and ``get_details`` retry transparently on transient
    HTTP / network errors — 5xx responses (502/503/504/500) and
    ``httpx.TransportError`` subclasses (timeouts, connection resets, broken
    pipes). One bad poll out of thousands shouldn't fail a long-running
    parent session.

    This helper has no overall timeout of its own — wrap the call in
    :func:`asyncio.wait_for` if you want a ceiling.

    Args:
        session: A Chronos child session (typically ``AsyncChronosSession``
            from ``chronos.launch(...)``).
        poll_interval: Status-poll period.
        heartbeat_interval: Heartbeat-log period.
        stage_label: Human-readable label for the child workload used in the
            heartbeat message (e.g. ``"explore"``, ``"testcase"``).
        chronos_base_url: Chronos base URL (e.g. ``ctx.chronos.base_url``);
            used to build ``session_url``.
        log_extra: Extra fields attached to each heartbeat record. Helper's
            own keys (``session_id``, ``status``, etc.) always win on
            collision.
        message_suffix: Trailing text appended to the heartbeat message.
            Callers that want to embed task IDs into the stderr line build
            the suffix themselves and pass it in.
        transient_max_attempts: Total attempts (including the first call)
            for each ``get_status`` / ``get_details`` invocation before a
            transient error is allowed to propagate. Default 5.
        transient_backoff_base: Initial backoff in seconds; doubles each
            attempt up to ``transient_backoff_cap`` with equal jitter.
        transient_backoff_cap: Maximum backoff in seconds between retries.
    """
    session_id = getattr(session, "session_id", None)
    plato_session_id = getattr(session, "plato_session_id", None)
    session_url = f"{chronos_base_url.rstrip('/')}/sessions/{session_id}" if chronos_base_url and session_id else None

    started_at = monotonic()
    next_heartbeat = heartbeat_interval

    while True:
        status_response = await _call_with_transient_retry(
            session.get_status,
            op_name="get_status",
            session_id=session_id,
            max_attempts=transient_max_attempts,
            backoff_base=transient_backoff_base,
            backoff_cap=transient_backoff_cap,
            log_extra=log_extra,
        )
        status_val = _status_str(status_response.status)
        if status_val in _TERMINAL_STATUSES:
            result = await _call_with_transient_retry(
                session.get_details,
                op_name="get_details",
                session_id=session_id,
                max_attempts=transient_max_attempts,
                backoff_base=transient_backoff_base,
                backoff_cap=transient_backoff_cap,
                log_extra=log_extra,
            )
            return _finalize_outcome(
                result,
                session_id=session_id,
                plato_session_id=plato_session_id,
                session_url=session_url,
            )

        elapsed = monotonic() - started_at
        if elapsed >= next_heartbeat:
            logger.debug(
                "Still waiting on %s session after %ds (status=%s)%s",
                stage_label,
                int(elapsed),
                status_val,
                message_suffix,
                extra={
                    **(log_extra or {}),
                    "session_id": session_id,
                    "session_url": session_url,
                    "elapsed_seconds": elapsed,
                    "status": status_val,
                    "status_reason": getattr(status_response, "status_reason", None),
                },
            )
            next_heartbeat += heartbeat_interval

        await asyncio.sleep(poll_interval)


def _finalize_outcome(
    result: SessionResponse,
    *,
    session_id: str | None,
    plato_session_id: str | None,
    session_url: str | None,
) -> ChildSessionOutcome:
    status = _status_str(result.status)
    resolved_plato_id = getattr(result, "plato_session_id", None) or plato_session_id
    if status != "completed":
        return ChildSessionOutcome(
            status=status,
            session_id=session_id,
            plato_session_id=resolved_plato_id,
            session_url=session_url,
            error=f"Session ended with status={status} reason={getattr(result, 'status_reason', None)}",
            details=result,
        )
    return ChildSessionOutcome(
        status=status,
        session_id=session_id,
        plato_session_id=resolved_plato_id,
        session_url=session_url,
        details=result,
    )


__all__ = [
    "ChildSessionOutcome",
    "DEFAULT_TRANSIENT_BACKOFF_BASE",
    "DEFAULT_TRANSIENT_BACKOFF_CAP",
    "DEFAULT_TRANSIENT_MAX_ATTEMPTS",
    "wait_for_child_session",
]
