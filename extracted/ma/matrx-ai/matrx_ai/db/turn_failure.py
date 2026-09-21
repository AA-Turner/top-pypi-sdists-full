"""Terminalize a turn whose stream task died before any finalizer ran.

THE COMPONENT THAT CATCHES THE CRASH OWNS THE TRUTH OF THE TURN.

``matrx_connect.streaming.response`` catches the stream task's crash and emits an
honest terminal error. That emit is live-only. On 2026-09-12 a journal write
timeout killed a conversation task mid-build: the user's screen went silent, and
on reload the transcript simply STOPPED after a tool_result while the request row
still read ``status=completed finish_reason=tool_calls`` — the status its last
successful iteration had left behind.

The orchestrator's own failure persistence
(``persistence.py`` ``_request_failed`` branch) is correct but unreachable here:
an escaping crash never calls ``persist_completed_request``, and its reserved
placeholder only ever covers the FIRST assistant position, so a turn that dies
after a tool_result has no row to close.

So this is the seam matrx-connect calls on that branch. It writes ONE failed
assistant row through the SAME writer that lands normal assistant rows, and marks
the request failed. It NEVER raises; it reports whether anything durable landed
so the caller can scream when nothing did.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from matrx_utils import vcprint

from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION

__all__ = ["persist_stream_turn_failure", "register_turn_failure_persister"]


def _queue_message_create(**kwargs: Any) -> str:
    from matrx_ai.persistence.queue_helpers import queue_message_create as _q

    return _q(**kwargs)


def _active_lane_coordinator() -> Any:
    from matrx_ai.db.conversation_gate import _get_active_lane_coordinator

    return _get_active_lane_coordinator()


async def _organization_for_failed_turn(conversation_id: str) -> str | None:
    """The organization the dead-turn row is written under, or ``None``.

    🚨 ``chat.message.organization_id`` is NOT NULL. Until 2026-09-20 this
    seam built ``fields`` with no organization at all — a sibling of the
    ``chat.agent_run`` bug fixed the same night in ``_checkpoint.py`` — so a
    stream crash on an org-scoped conversation would fail a SECOND time
    trying to record the first failure, hiding the real crash behind a raw
    23502 instead of showing the user why their turn stopped.

    This runs on the out-of-lane crash branch, where the request that verified
    an organization may already be long gone — the stream task that died could
    have outlived the request by minutes. So there is exactly one legitimate
    source here: the PARENT conversation row's own ``organization_id`` — a
    failed-turn message is a child of that conversation, never of "whoever
    happens to still be in scope" — read fresh rather than trusted from a
    context that might not exist any more. Never a default, never a lookup by
    user; a conversation that cannot be read yields ``None`` and the caller
    refuses the write rather than let a null reach Postgres.
    """
    try:
        from matrx_ai.db import cxm

        rows = await cxm.conversation.filter_items(id=conversation_id)
    except Exception as exc:  # noqa: BLE001 - this seam never raises
        vcprint(
            f"[TURN FAILURE] Could not read organization_id off conversation "
            f"{conversation_id}: {exc}",
            color="yellow",
        )
        return None
    if not rows:
        return None
    org = getattr(rows[0], "organization_id", None)
    return str(org).strip() if org else None


async def persist_stream_turn_failure(
    *,
    conversation_id: str,
    request_id: str | None,
    user_id: str | None,
    error_type: str,
    message: str,
    user_message: str,
    route: str,
    **_extra: Any,
) -> bool:
    """Write the dead turn's durable trace. Returns True if a row landed.

    The row is deliberately shaped like every other failed assistant turn so the
    chat UI renders it with no new frontend concept:
      * ``status='failed'`` and a structured ``error`` — either one alone is
        enough for the client's ``isFailedRecord`` predicate.
      * ``is_visible_to_user=True`` so the person sees why their turn stopped.
      * ``is_visible_to_model=False`` so the agent does not re-read its own
        infrastructure failure as if it were content.
      * the honest user-facing text as the content, identical to the wire.
    """
    if not conversation_id:
        return False

    row_id = str(uuid4())
    error_struct: dict[str, Any] = {
        "type": error_type or "stream_crash",
        "message": message or user_message,
    }
    if request_id:
        error_struct["request_id"] = request_id
    # chat.message.organization_id is NOT NULL. See
    # `_organization_for_failed_turn` for why the PARENT conversation row is the
    # only source trusted here — this branch runs after a crash, possibly long
    # after the request that verified an organization has ended.
    organization_id = await _organization_for_failed_turn(conversation_id)
    fields: dict[str, Any] = {
        "id": row_id,
        "conversation_id": conversation_id,
        "role": "assistant",
        "position": APPEND_MESSAGE_POSITION,
        "status": "failed",
        "is_visible_to_user": True,
        "is_visible_to_model": False,
        "content": [{"type": "text", "text": user_message or message}],
        "error": error_struct,
        "created_by": user_id or None,
        "organization_id": organization_id,
    }

    wrote_message = False
    if organization_id is None:
        # No default, no lookup by user — the write must not happen. This is
        # the background path the class of bug names explicitly: refuse
        # loudly (never a silent no-op, never a null reaching Postgres) and
        # let the caller's own "nothing landed" handling scream.
        vcprint(
            f"[TURN FAILURE] Could not determine organization_id for conversation "
            f"{conversation_id}; the failed-turn row was NOT written "
            f"(chat.message.organization_id is NOT NULL). The conversation row "
            f"may itself be missing or org-less.",
            color="red",
        )
    elif _active_lane_coordinator() is not None:
        # In-lane: the ordinary writer. The coordinator flushes on drain, and
        # the streaming wrapper drains AFTER this handler returns.
        try:
            _queue_message_create(**fields)
            wrote_message = True
        except Exception as exc:  # noqa: BLE001
            vcprint(
                f"[TURN FAILURE] Could not queue the failed-turn row for "
                f"conversation {conversation_id}: {exc}",
                color="yellow",
            )
    else:
        wrote_message = await _direct_write_failed_message(fields, conversation_id)

    # The request row's terminal status. Independent of the message write: a
    # request left reading 'completed' for a turn that died is its own lie.
    if request_id:
        try:
            from matrx_ai.db.conversation_gate import update_user_request_status

            await update_user_request_status(
                request_id,
                "failed",
                error=message or user_message,
            )
        except Exception as exc:  # noqa: BLE001 - already fire-and-forget safe
            vcprint(
                f"[TURN FAILURE] Could not mark request {request_id} failed: {exc}",
                color="yellow",
            )

    if wrote_message:
        vcprint(
            f"[TURN FAILURE] {route}: persisted the dead turn as a failed "
            f"assistant row ({row_id}) in conversation {conversation_id}.",
            color="yellow",
        )
    return wrote_message


async def _direct_write_failed_message(
    fields: dict[str, Any], conversation_id: str
) -> bool:
    """Out-of-lane branch: a governed one-shot write, same as the gate uses.

    A crash can land after the request's lane has already drained, and a drained
    lane is not ownership — materializing a coordinator there records
    ``persistence_after_lane_drain`` instead of writing. chat.message is
    Coordinator-owned, so the bypass is acknowledged explicitly rather than
    tripping a false ownership alarm.
    """
    try:
        from matrx_orm import (
            COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
            Session,
            allow_direct_coordinator_write,
        )

        from matrx_ai.db import cxm

        manager = cxm.message
        with allow_direct_coordinator_write(
            manager.model,
            reason=(
                "out-of-lane failed-turn row — the stream task died after its "
                "lane drained and the turn must not vanish from the transcript"
            ),
            acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
        ):
            async with Session():
                await manager.create_item(**fields)
        return True
    except Exception as exc:  # noqa: BLE001 - the caller screams; we never raise
        vcprint(
            f"[TURN FAILURE] Direct write of the failed-turn row for "
            f"conversation {conversation_id} failed: {exc}",
            color="yellow",
        )
        return False


def register_turn_failure_persister() -> None:
    """Install this package's persister into the matrx-connect crash branch."""
    try:
        from matrx_connect.streaming.turn_failure import (
            configure_turn_failure_persister,
        )
    except ImportError:  # pragma: no cover - older matrx-connect
        return
    configure_turn_failure_persister(persist_stream_turn_failure)
