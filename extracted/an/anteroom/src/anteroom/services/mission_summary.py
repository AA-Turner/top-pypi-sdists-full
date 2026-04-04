"""Mission delta summaries and retrospectives (#1263).

Provides aggregation helpers for mission event streams:
- ``build_delta_summary`` — incremental summary since a given timestamp
- ``build_retrospective`` — full narrative of planned vs actual outcomes
- ``generate_and_store_retrospective`` — builds and stores as an event
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

logger = logging.getLogger(__name__)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(ts: str) -> datetime:
    """Parse an ISO 8601 timestamp, tolerating missing timezone."""
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.now(timezone.utc)


def _duration_seconds(start: str, end: str) -> float:
    return max(0.0, (_parse_iso(end) - _parse_iso(start)).total_seconds())


# ---------------------------------------------------------------------------
# Delta summary
# ---------------------------------------------------------------------------


def build_delta_summary(
    db: ThreadSafeConnection,
    session_id: str,
    since: str | None = None,
) -> dict[str, Any]:
    """Aggregate events since *since* (ISO 8601) into a delta summary.

    If *since* is ``None``, all events for the session are included.
    """
    from . import mission_storage as ms

    if since:
        events = ms.list_events_since(db, session_id, since)
    else:
        events = ms.list_events(db, session_id, limit=10000)

    launched: list[str] = []
    completed: list[str] = []
    failed: list[str] = []
    other_transitions: list[dict[str, Any]] = []

    for ev in events:
        item_id = ev.get("item_id")
        etype = ev.get("event_type", "")
        detail = ev.get("detail") or {}

        if etype == "item_launched" and item_id:
            launched.append(item_id)
        elif etype == "item_completed" and item_id:
            completed.append(item_id)
        elif etype == "item_failed" and item_id:
            failed.append(item_id)
        elif item_id:
            other_transitions.append({"item_id": item_id, "event_type": etype, "detail": detail})

    session_events = [ev for ev in events if ev.get("event_type", "").startswith("session_")]

    return {
        "session_id": session_id,
        "since": since,
        "event_count": len(events),
        "items_launched": launched,
        "items_completed": completed,
        "items_failed": failed,
        "other_transitions": other_transitions,
        "session_events": [{"event_type": ev["event_type"], "created_at": ev["created_at"]} for ev in session_events],
    }


# ---------------------------------------------------------------------------
# Retrospective
# ---------------------------------------------------------------------------


def build_retrospective(
    db: ThreadSafeConnection,
    session_id: str,
) -> dict[str, Any]:
    """Build a full retrospective for a mission session.

    Compares planned items against actual outcomes: completion rate,
    failures, durations, and key events.
    """
    from . import mission_storage as ms

    session = ms.get_session(db, session_id)
    if session is None:
        raise ValueError(f"Session not found: {session_id}")

    items = ms.list_items_by_session(db, session_id)
    events = ms.list_events(db, session_id, limit=10000)

    total = len(items)
    completed_items = [i for i in items if i["status"] == "completed"]
    failed_items = [i for i in items if i["status"] == "failed"]
    dropped_items = [i for i in items if i["status"] == "dropped"]

    completion_rate = (len(completed_items) / total * 100.0) if total > 0 else 0.0

    # Duration: session created_at to now (or last event)
    start_ts = session["created_at"]
    end_ts = events[-1]["created_at"] if events else _now()
    duration_s = _duration_seconds(start_ts, end_ts)

    # Per-item durations from launched to terminal event
    item_durations: dict[str, float] = {}
    launch_times: dict[str, str] = {}
    for ev in events:
        item_id = ev.get("item_id")
        if not item_id:
            continue
        etype = ev.get("event_type", "")
        if etype == "item_launched":
            launch_times[item_id] = ev["created_at"]
        elif etype in ("item_completed", "item_failed", "item_cancelled") and item_id in launch_times:
            item_durations[item_id] = _duration_seconds(launch_times[item_id], ev["created_at"])

    return {
        "session_id": session_id,
        "title": session.get("title"),
        "status": session["status"],
        "total_items": total,
        "completed": len(completed_items),
        "failed": len(failed_items),
        "dropped": len(dropped_items),
        "completion_rate": round(completion_rate, 1),
        "duration_seconds": round(duration_s, 1),
        "item_durations": item_durations,
        "failed_summaries": [i["summary"] for i in failed_items],
        "completed_summaries": [i["summary"] for i in completed_items],
        "event_count": len(events),
    }


# ---------------------------------------------------------------------------
# Generate and store
# ---------------------------------------------------------------------------


def generate_and_store_retrospective(
    db: ThreadSafeConnection,
    session_id: str,
    *,
    is_draft: bool = False,
) -> dict[str, Any]:
    """Build a retrospective and store it as a mission event.

    Draft retrospectives (``is_draft=True``) use event type
    ``session_retrospective_draft`` and are superseded if the session
    later recovers and completes. Final retrospectives use
    ``session_retrospective``.
    """
    from . import mission_storage as ms

    retro = build_retrospective(db, session_id)
    event_type = "session_retrospective_draft" if is_draft else "session_retrospective"

    if not is_draft:
        ms.delete_events_by_type(db, session_id, "session_retrospective_draft")

    event = ms.create_event(
        db,
        session_id=session_id,
        event_type=event_type,
        detail=retro,
    )

    logger.info(
        "Stored %s for session %s (completion_rate=%.1f%%)",
        event_type,
        session_id[:8],
        retro["completion_rate"],
    )

    return event
