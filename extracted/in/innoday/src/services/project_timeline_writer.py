"""
Shared helper for writing ProjectTimeline entries from mutation points
across the codebase (board registration, repo sync, release lifecycle,
ticket sync batches). Kept intentionally tiny -- this is not a service with
business logic, just a single place to construct the row consistently so
every call site doesn't repeat the same six-field constructor.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from sqlmodel import Session, select

from src.domain.project_timeline import ProjectTimeline, TimelineEventType


def add_timeline_entry(
    session: Session,
    *,
    organization_id: str,
    project_id: str,
    event_type: TimelineEventType,
    title: str,
    summary: str,
    created_by: str = "system",
    metadata: Optional[Dict[str, Any]] = None,
) -> ProjectTimeline:
    """
    Add a ProjectTimeline row. Does not commit -- callers add this to their
    existing transaction and commit alongside the rest of their mutation,
    so the timeline entry and the change it describes land atomically.
    """
    entry = ProjectTimeline(
        organization_id=organization_id,
        project_id=project_id,
        event_type=event_type,
        title=title,
        summary=summary,
        occurred_at=datetime.now(timezone.utc),
        created_by=created_by,
        metadata_json=metadata,
    )
    session.add(entry)
    return entry


def upsert_daily_timeline_entry(
    session: Session,
    *,
    organization_id: str,
    project_id: str,
    event_type: TimelineEventType,
    title: str,
    summary: str,
    created_by: str = "system",
    metadata: Optional[Dict[str, Any]] = None,
    now: Optional[datetime] = None,
) -> ProjectTimeline:
    """At most one entry of this type, on this project, per UTC calendar day.

    For events that are a **standing snapshot** rather than a discrete
    happening. A scrum summary is the example: re-running it at 09:00 and again
    at 16:00 does not mean the team stood up twice, it means the same day's
    picture was taken again, and a feed carrying both reads as two stand-ups.
    Appending is right for a release or a repo attach -- those really did happen
    twice -- so this is a second function, not a change to `add_timeline_entry`.

    The surviving row is rewritten to the latest snapshot, `occurred_at`
    included: the entry states where the project stood *as of* that moment, and
    freezing it at the day's first write would leave the timestamp describing a
    body of text that has since been replaced.

    Same transaction discipline as `add_timeline_entry` -- no commit here.

    The day is bounded with an explicit `[midnight, midnight+1day)` range rather
    than a `date()`/`DATE_TRUNC` cast so the existing
    `ix_project_timeline_project_occurred_at` index still serves the lookup; a
    function over the column would not be sargable against it.
    """
    now = now or datetime.now(timezone.utc)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    # `occurred_at` is `DateTime(timezone=True)` and every writer passes an
    # aware UTC value, so the bounds stay aware too -- Postgres will not compare
    # an aware column against a naive literal.
    existing = session.exec(
        select(ProjectTimeline)
        .where(
            ProjectTimeline.project_id == project_id,
            ProjectTimeline.event_type == event_type,
            ProjectTimeline.occurred_at >= day_start,
            ProjectTimeline.occurred_at < day_end,
        )
        .order_by(ProjectTimeline.occurred_at.desc())
    ).first()

    if existing is not None:
        existing.title = title
        existing.summary = summary
        existing.created_by = created_by
        existing.metadata_json = metadata
        existing.occurred_at = now
        session.add(existing)
        return existing

    return add_timeline_entry(
        session,
        organization_id=organization_id,
        project_id=project_id,
        event_type=event_type,
        title=title,
        summary=summary,
        created_by=created_by,
        metadata=metadata,
    )
