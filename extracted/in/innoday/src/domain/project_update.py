"""Project update domain models for tracking requirements changes and clarifications."""

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.project import Project
    from src.domain.scope_document import ScopeDocument


class UpdateType(str, Enum):
    """Types of project updates in the requirements workflow"""

    REQUIREMENT = "requirement"  # New or changed requirement
    CLARIFICATION = "clarification"  # Clarification of existing requirement
    FEEDBACK = "feedback"  # Client feedback on scope
    QUESTION = "question"  # Agent question needing answer
    ANSWER = "answer"  # Client answer to agent question


class ProjectUpdate(SQLModel, table=True):
    """
    Tracks iterative updates during project scoping.

    Captures the back-and-forth between client and agent
    during requirements gathering and scope refinement.
    """

    __tablename__ = "project_updates"

    # Identity
    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    project_id: str = Field(
        sa_column=Column(String, ForeignKey("projects.id"), index=True)
    )

    # Update details
    update_type: UpdateType = Field(description="Type of update in the workflow")
    content: str = Field(
        sa_column=Column(Text),
        description="The update content (requirement, question, etc.)",
    )

    # Scope document association
    scope_document_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String, ForeignKey("scope_documents.id")),
        description="Associated scope document version",
    )

    # Processing status
    processed: bool = Field(
        default=False, description="Whether this update has been processed"
    )
    processed_at: Optional[datetime] = Field(
        default=None, description="When the update was processed"
    )

    # Response tracking
    response: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
        description="Agent response or action taken",
    )
    requires_client_input: bool = Field(
        default=False, description="Whether this needs client response"
    )

    # Metadata
    context: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
        description="Additional context or metadata",
    )

    # Creator tracking
    created_by: str = Field(description="User ID or 'agent' for AI-generated")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    project: Optional["Project"] = Relationship(back_populates="updates")
    scope_document: Optional["ScopeDocument"] = Relationship(back_populates="updates")

    def mark_processed(self, response: Optional[str] = None) -> None:
        """Mark this update as processed with optional response"""
        self.processed = True
        self.processed_at = datetime.now(timezone.utc)
        if response:
            self.response = response
        self.updated_at = datetime.now(timezone.utc)
