"""Project timeline domain model — a curated, human-readable event history.

Distinct from ProjectUpdate (src/domain/project_update.py), which tracks the
requirements-scoping back-and-forth (requirement/clarification/feedback/
question/answer) and is not touched by this model. A timeline entry is a
short narrative record of something that happened on a project — a release,
a meeting, a scrum summary — meant to be read chronologically by anyone
joining mid-stream, not a workflow item to be processed and resolved.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Index, String, Text, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.organization import Organization
    from src.domain.project import Project


class TimelineEventType(str, Enum):
    """What kind of event this timeline entry records."""

    RELEASE = "release"
    MEETING = "meeting"
    SPEC_UPDATE = "spec_update"
    SCRUM_SUMMARY = "scrum_summary"
    REPO_ADDED = "repo_added"
    REPO_REMOVED = "repo_removed"
    TICKET_SYNC = "ticket_sync"
    RELEASE_CREATED = "release_created"
    RELEASE_UPDATED = "release_updated"
    BOARD_ATTACHED = "board_attached"


class ProjectTimeline(SQLModel, table=True):
    """
    A single entry in a project's curated event history.

    `summary` is always plain language, 2-3 sentences — written for someone
    with no context on the underlying ticket/PR/commit data. `metadata` holds
    the structured detail (ticket IDs, PR numbers, version strings, per-repo
    breakdowns) for anyone who wants to drill in; it is never required to
    understand the entry.
    """

    __tablename__ = "project_timeline"

    # The timeline feed's only real read pattern is "this project, newest
    # first" (GET .../timeline, paginated). The migration built the index in
    # that direction; declaring it here keeps `create_all` -- which the test
    # fixtures use -- building the same schema production runs.
    __table_args__ = (
        Index(
            "ix_project_timeline_project_occurred_at",
            "project_id",
            text("occurred_at DESC"),
        ),
    )

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    # `ondelete="CASCADE"` on both FKs: deleting an org or a project takes its
    # timeline with it, which is what the migration built. Without it stated
    # here, `alembic revision --autogenerate` emits a migration that DROPs the
    # cascade off production.
    organization_id: str = Field(
        sa_column=Column(
            String,
            ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )
    project_id: str = Field(
        sa_column=Column(
            String,
            ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    event_type: TimelineEventType = Field(description="What kind of event this is")
    title: str = Field(max_length=255, description="Short, human-readable title")
    # An entry with no summary is not a timeline entry -- the whole point of
    # the row is the plain-language narrative. Production has it NOT NULL;
    # `sa_column=` drops SQLModel's inference, so it has to be said here.
    summary: str = Field(
        sa_column=Column(Text, nullable=False),
        description="2-3 sentence plain-language summary of what happened",
    )

    # Timezone-aware on both timestamp columns: the values written are
    # `datetime.now(timezone.utc)`, and a naive column would silently drop the
    # offset on the way in and hand back a naive value on the way out.
    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
        description="When the event happened (not when the row was written)",
    )

    created_by: str = Field(
        description="User ID, or 'agent'/skill name for AI-generated entries"
    )

    metadata_json: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column("metadata", JSON),
        description="Structured detail: ticket IDs, PR numbers, version, per-repo breakdown, etc.",
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    organization: Optional["Organization"] = Relationship()
    project: Optional["Project"] = Relationship(back_populates="timeline_entries")
