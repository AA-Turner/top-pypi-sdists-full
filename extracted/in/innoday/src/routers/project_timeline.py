"""
Project Timeline API Router (PF-102)

A curated, human-readable event history for a project — releases, meetings,
spec updates, scrum summaries, repo additions. Distinct from ProjectUpdate
(src/routers/projects.py's /updates endpoints), which tracks the
requirements-scoping workflow and is untouched by this router.
"""

import base64
import binascii
import logging
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from src.database import get_session
from src.domain.organization import Organization
from src.domain.project_timeline import ProjectTimeline, TimelineEventType
from src.domain.user import User
from src.middleware.rbac import get_current_user, require_org_role
from src.routers.projects import resolve_project

logger = logging.getLogger(__name__)

router = APIRouter(tags=["project-timeline"])

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class TimelineEntryCreate(BaseModel):
    event_type: TimelineEventType
    title: str = Field(..., max_length=255)
    summary: str = Field(..., description="2-3 sentence plain-language summary")
    occurred_at: Optional[datetime] = Field(
        None, description="When the event happened; defaults to now"
    )
    created_by: str = Field(..., description="User ID, or 'agent'/skill name")
    metadata: Optional[dict] = Field(
        None, description="Structured detail: ticket IDs, PR numbers, version, etc."
    )


class TimelineEntryResponse(BaseModel):
    id: str
    organization_id: str
    project_id: str
    event_type: TimelineEventType
    title: str
    summary: str
    occurred_at: datetime
    created_by: str
    metadata: Optional[dict] = None
    created_at: datetime


class TimelineListResponse(BaseModel):
    entries: List[TimelineEntryResponse]
    next_cursor: Optional[str] = None


# ---------------------------------------------------------------------------
# Cursor helpers
# ---------------------------------------------------------------------------


def _encode_cursor(occurred_at: datetime, entry_id: str) -> str:
    raw = f"{occurred_at.isoformat()}|{entry_id}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def _decode_cursor(cursor: str) -> tuple:
    try:
        raw = base64.urlsafe_b64decode(cursor.encode()).decode()
        occurred_at_str, entry_id = raw.split("|", 1)
        return datetime.fromisoformat(occurred_at_str), entry_id
    except (ValueError, binascii.Error) as e:
        raise HTTPException(status_code=400, detail=f"Invalid cursor: {e}")


def _entry_to_response(e: ProjectTimeline) -> TimelineEntryResponse:
    return TimelineEntryResponse(
        id=e.id,
        organization_id=e.organization_id,
        project_id=e.project_id,
        event_type=e.event_type,
        title=e.title,
        summary=e.summary,
        occurred_at=e.occurred_at,
        created_by=e.created_by,
        metadata=e.metadata_json,
        created_at=e.created_at,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/api/v1/organizations/{org_id}/projects/{project_id}/timeline",
    response_model=TimelineEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_timeline_entry(
    org_id: str,
    project_id: str,
    body: TimelineEntryCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Add an entry to a project's timeline."""
    # Alias or id, like every other project-scoped route. The CLI's `--project`
    # takes an alias everywhere else, so a UUID-only lookup here would answer
    # "Project not found" for a project the caller administers.
    project = resolve_project(project_id, org_id, session)

    entry = ProjectTimeline(
        organization_id=org_id,
        project_id=project.id,
        event_type=body.event_type,
        title=body.title,
        summary=body.summary,
        occurred_at=body.occurred_at or datetime.now(timezone.utc),
        created_by=body.created_by,
        metadata_json=body.metadata,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return _entry_to_response(entry)


@router.get(
    "/api/v1/organizations/{org_id}/projects/{project_id}/timeline",
    response_model=TimelineListResponse,
)
async def get_project_timeline(
    org_id: str,
    project_id: str,
    event_type: Optional[TimelineEventType] = Query(None),
    cursor: Optional[str] = Query(
        None, description="Opaque cursor from a previous response's next_cursor"
    ),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get a project's timeline, newest first.

    Cursor-paginated: pass the previous response's `next_cursor` to get the
    next page. `next_cursor` is null when there are no more entries.
    """
    # Alias or id, like every other project-scoped route. The CLI's `--project`
    # takes an alias everywhere else, so a UUID-only lookup here would answer
    # "Project not found" for a project the caller administers.
    project = resolve_project(project_id, org_id, session)

    q = select(ProjectTimeline).where(ProjectTimeline.project_id == project.id)
    if event_type:
        q = q.where(ProjectTimeline.event_type == event_type)

    if cursor:
        cursor_occurred_at, cursor_id = _decode_cursor(cursor)
        # Strict "older than the cursor row" — (occurred_at, id) as a composite
        # tie-breaker so entries with an identical occurred_at don't repeat or
        # get skipped across pages.
        q = q.where(
            (ProjectTimeline.occurred_at < cursor_occurred_at)
            | (
                (ProjectTimeline.occurred_at == cursor_occurred_at)
                & (ProjectTimeline.id < cursor_id)
            )
        )

    q = q.order_by(ProjectTimeline.occurred_at.desc(), ProjectTimeline.id.desc()).limit(
        limit + 1
    )
    rows = session.exec(q).all()

    has_more = len(rows) > limit
    page = rows[:limit]

    next_cursor = None
    if has_more and page:
        last = page[-1]
        next_cursor = _encode_cursor(last.occurred_at, last.id)

    return TimelineListResponse(
        entries=[_entry_to_response(e) for e in page],
        next_cursor=next_cursor,
    )
