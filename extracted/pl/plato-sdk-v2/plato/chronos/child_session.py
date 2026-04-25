"""Heartbeat-aware wait loop for child Chronos sessions.

Worlds that launch child worlds (e.g. CUA benchmark sessions) need more than
``wait_until_complete``: they want heartbeat logs, a constructed session URL,
and the raw ``SessionResponse`` passed through so the world can map it into
its own result schema.

Timeouts are the caller's concern — wrap in :func:`asyncio.wait_for` if you
want a ceiling. The SDK keeps polling until Chronos reports a terminal
status.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from time import monotonic
from typing import TYPE_CHECKING

from plato.chronos.models import SessionResponse

if TYPE_CHECKING:
    from plato.chronos.sdk import AsyncChronosSession

logger = logging.getLogger(__name__)

_TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled", "error"})


def _status_str(status: object) -> str:
    value = getattr(status, "value", None)
    return value if isinstance(value, str) else str(status)


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
) -> ChildSessionOutcome:
    """Wait for a Chronos child session to reach a terminal status.

    Polls ``session.get_status`` until the session reports a terminal status,
    then fetches ``session.get_details``. Heartbeat logs are emitted every
    ``heartbeat_interval`` seconds via ``plato.chronos.child_session`` at
    DEBUG level (so Chronos marks them ``plato.debug=True`` and hides them in
    the default trace view, and stderr stays quiet during long waits).

    This helper has no timeout of its own — wrap the call in
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
    """
    session_id = getattr(session, "session_id", None)
    plato_session_id = getattr(session, "plato_session_id", None)
    session_url = f"{chronos_base_url.rstrip('/')}/sessions/{session_id}" if chronos_base_url and session_id else None

    started_at = monotonic()
    next_heartbeat = heartbeat_interval

    while True:
        status_response = await session.get_status()
        status_val = _status_str(status_response.status)
        if status_val in _TERMINAL_STATUSES:
            result = await session.get_details()
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


__all__ = ["ChildSessionOutcome", "wait_for_child_session"]
