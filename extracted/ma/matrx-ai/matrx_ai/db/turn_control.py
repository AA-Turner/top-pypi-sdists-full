"""Durable pause / resume for a running turn, carried by the Turn-Boundary Inbox.

A ``turn_control`` row is a CONTROL item, never a message: no drain delivers it to the model and no
list shows it as queued. It rides the inbox because that is the durable delivery that reaches
whichever server task runs the turn; the task reads it at its next drain point (and while held) and
applies it to its own request tree (``tools/dynamic_drain.apply_turn_controls``).
"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from typing import Any

#: The inbox row ``kind`` of a pause / resume item (``content = {"op": "pause"|"resume", "request_id": ...}``).
TURN_CONTROL_KIND = "turn_control"
#: The hold timings are ``platform.feature_knob`` rows (feature ``agents.turn_control``), read live
#: through the package knob seam (``matrx_ai.knobs``); the numbers below are the seeded row values.
TURN_CONTROL_KNOB_FEATURE = "agents.turn_control"


def control_stale_seconds() -> float:
    """A control item nobody took within this many seconds is stale (its turn ended): consumed unapplied."""
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(TURN_CONTROL_KNOB_FEATURE, "control_stale_seconds", 600.0, low=30.0, high=86400.0)  # KNOB MIRROR agents.turn_control.control_stale_seconds


def pause_max_hold_seconds() -> float:
    """Longest a paused turn is held before it continues on its own (announced)."""
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(TURN_CONTROL_KNOB_FEATURE, "pause_max_hold_seconds", 3600.0, low=60.0, high=86400.0)  # KNOB MIRROR agents.turn_control.pause_max_hold_seconds


def control_poll_seconds() -> float:
    """How often a HELD turn reads resume / pause / Stop sent from another server task."""
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(TURN_CONTROL_KNOB_FEATURE, "control_poll_seconds", 1.0, low=0.25, high=10.0)  # KNOB MIRROR agents.turn_control.control_poll_seconds


async def claim_turn_control_rows(
    store: Any, conversation_id: str, *, request_ids: set[str], request_id: str | None = None
) -> list[Any]:
    """Atomically claim the control items addressed to THIS run (``content.request_id`` in
    ``request_ids``), FIFO. ``store`` is the inbox manager (``filter_items`` / ``update_where``).
    Items for another run stay pending for it; stale items are consumed unapplied, so a control for
    a turn that already ended can never pause the next one."""
    rows = await store.filter_items(conversation_id=conversation_id, kind=TURN_CONTROL_KIND, status="pending")
    mine: list[Any] = []
    stale_after = control_stale_seconds()
    for row in sorted(rows, key=lambda r: int(getattr(r, "enqueued_seq", 0) or 0)):
        content = row.content if isinstance(row.content, dict) else {}
        created = getattr(row, "created_at", None)
        stale = created is not None and time.time() - created.timestamp() > stale_after
        if not stale and str(content.get("request_id") or "") not in request_ids:
            continue
        result = await store.update_where(
            {"id": str(row.id), "status": "pending"},
            status="consumed",
            consumed_at=datetime.now(UTC),
            consumed_by_request_id=request_id,
        )
        if not stale:
            mine.extend(result.updated_rows or [])
    return mine
