"""Models for Deep Research Report Versions."""
import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship

from ...database import Base


class ReportVersionStatusEnum(enum.Enum):
    """Status enum for deep research report revisions."""
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DeepResearchReportVersionModel(Base):
    """
    Immutable revision metadata for deep research report outputs.
    """

    __tablename__ = "deep_research_report_versions"

    id = Column(Integer, primary_key=True)

    session_id = Column(
        Integer,
        ForeignKey("deep_research_sessions.id"),
        nullable=False,
    )

    revision_id = Column(String(64), nullable=False)
    version_number = Column(Integer, nullable=False)
    mode = Column(String(32), nullable=True)  # initial | report_refine | evidence_gap | mixed
    status = Column(
        "status",
        Enum(ReportVersionStatusEnum),
        default=ReportVersionStatusEnum.IN_PROGRESS,
        nullable=False,
    )

    parent_report_version_id = Column(
        Integer,
        ForeignKey("deep_research_report_versions.id"),
        nullable=True,
    )

    feedback_payload = Column(Text, nullable=True)  # JSON
    execution_arn = Column(String(512), nullable=True)
    final_report_s3_key = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)

    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
    completed_at = Column(DateTime, nullable=True)

    parent_report_version = relationship(
        "DeepResearchReportVersionModel",
        remote_side=[id],
        backref="child_report_versions",
        foreign_keys=[parent_report_version_id],
    )
