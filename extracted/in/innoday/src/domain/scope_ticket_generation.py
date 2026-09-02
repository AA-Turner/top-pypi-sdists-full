"""
Scope ticket generation tracking model.

Tracks ticket generation from scope documents to prevent duplicates and provide audit trail.
Follows the pattern established by BoardSyncHistory and Summary.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import JSON, ForeignKey, String
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:  # forward refs for the Relationship() strings below
    from .board import BoardRegistration
    from .organization import Organization
    from .project import Project
    from .scope_document import ScopeDocument
    from .user import User


class GenerationStatus(str, Enum):
    """Status of ticket generation operation"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ScopeTicketGeneration(SQLModel, table=True):
    """
    Tracks ticket generation from scope documents.

    Similar to BoardSyncHistory but for scope → ticket generation.
    Prevents duplicate generations and provides audit trail.
    """

    __tablename__ = "scope_ticket_generations"

    # Primary key
    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )

    # Foreign keys
    scope_document_id: str = Field(
        sa_column=Column(String, ForeignKey("scope_documents.id"))
    )
    project_id: str = Field(sa_column=Column(String, ForeignKey("projects.id")))
    organization_id: str = Field(
        sa_column=Column(String, ForeignKey("organizations.id"))
    )
    board_registration_id: str = Field(
        sa_column=Column(String, ForeignKey("board_registrations.id"))
    )

    # Generation results (similar to BoardSyncHistory)
    status: GenerationStatus = Field(default=GenerationStatus.PENDING)
    tickets_generated: int = Field(default=0, description="Total tickets created")
    epics_created: int = Field(default=0)
    stories_created: int = Field(default=0)
    tasks_created: int = Field(default=0)

    # Tracking data (similar to Summary JSON fields)
    ticket_ids: List[str] = Field(
        default_factory=list, sa_column=Column(JSON), description="InnoDay ticket IDs"
    )
    external_ticket_ids: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON),
        description="External board ticket IDs (Jira keys, Trello card IDs)",
    )
    epic_mapping: Dict[str, List[str]] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="epic_id -> [story_ids] mapping for hierarchy",
    )

    # Error handling
    error_message: Optional[str] = Field(default=None)

    # Timestamps (following BoardSyncHistory pattern)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # User tracking
    created_by: str = Field(sa_column=Column(String, ForeignKey("users.id")))

    # Relationships
    scope_document: Optional["ScopeDocument"] = Relationship()
    project: Optional["Project"] = Relationship()
    organization: Optional["Organization"] = Relationship()
    board_registration: Optional["BoardRegistration"] = Relationship()
    user: Optional["User"] = Relationship()

    @property
    def duration_seconds(self) -> Optional[int]:
        """Calculate generation duration in seconds"""
        if self.completed_at and self.started_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return None

    def mark_completed(
        self,
        status: GenerationStatus,
        tickets_generated: int = 0,
        error_message: Optional[str] = None,
    ) -> None:
        """Mark generation as completed (success or failure)"""
        self.status = status
        self.tickets_generated = tickets_generated
        self.completed_at = datetime.now(timezone.utc)
        if error_message:
            self.error_message = error_message
