"""Scope document domain models for project requirements and refinement."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.project import Project
    from src.domain.project_update import ProjectUpdate


class ScopeStatus(str, Enum):
    """Status of a scope document in the refinement workflow"""

    DRAFT = "draft"  # Initial or being edited
    IN_REVIEW = "in_review"  # Under review/refinement
    FINAL = "final"  # Ready for project approval


class ScopeDocument(SQLModel, table=True):
    """
    Versioned scope documents for projects.

    Captures original requirements and refined scope through
    an iterative refinement process with agent assistance.
    """

    __tablename__ = "scope_documents"

    # Identity
    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )
    project_id: str = Field(
        sa_column=Column(String, ForeignKey("projects.id"), index=True)
    )

    # Versioning
    version: int = Field(default=1)
    is_current: bool = Field(
        default=True, description="Whether this is the current active version"
    )

    # Status
    status: ScopeStatus = Field(default=ScopeStatus.DRAFT)

    # Content
    requirements: str = Field(
        sa_column=Column(Text), description="Original client requirements"
    )
    refined_scope: str = Field(
        sa_column=Column(Text), description="Agent-refined and clarified scope"
    )

    # Deliverables and constraints
    deliverables: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
        description="Markdown-formatted list of deliverables",
    )
    success_criteria: Optional[str] = Field(
        default=None, sa_column=Column(Text), description="Measurable success criteria"
    )
    assumptions: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
        description="Key assumptions made during scoping",
    )
    exclusions: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
        description="What's explicitly out of scope",
    )

    # Estimates
    estimated_hours: Optional[int] = Field(
        default=None, description="Total estimated hours for completion"
    )
    estimated_cost: Optional[float] = Field(
        default=None, description="Estimated cost based on hours and rates"
    )

    # Technical details
    technical_requirements: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
        description="Technical stack, dependencies, constraints",
    )

    # Agent refinement metadata
    clarification_rounds: int = Field(
        default=0, description="Number of Q&A rounds with client"
    )
    confidence_score: Optional[float] = Field(
        default=None, description="Agent's confidence in scope completeness (0-1)"
    )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    finalized_at: Optional[datetime] = Field(
        default=None, description="When status became FINAL"
    )

    # Creator tracking
    created_by: str = Field(description="User ID or 'agent' for AI-generated")

    # Relationships
    project: Optional["Project"] = Relationship(back_populates="scope_documents")
    updates: list["ProjectUpdate"] = Relationship(back_populates="scope_document")

    # Constraints
    __table_args__ = (
        UniqueConstraint("project_id", "version", name="uq_scope_project_version"),
    )

    def create_new_version(self) -> "ScopeDocument":
        """Create a new version based on this document"""
        return ScopeDocument(
            project_id=self.project_id,
            version=self.version + 1,
            status=ScopeStatus.DRAFT,
            requirements=self.requirements,
            refined_scope=self.refined_scope,
            deliverables=self.deliverables,
            success_criteria=self.success_criteria,
            assumptions=self.assumptions,
            exclusions=self.exclusions,
            estimated_hours=self.estimated_hours,
            estimated_cost=self.estimated_cost,
            technical_requirements=self.technical_requirements,
            created_by=self.created_by,
        )
