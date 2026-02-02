"""Models for Deep Research Sessions - Agentic research orchestration."""
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
    Float,
)
from sqlalchemy.orm import relationship

from ...database import Base


class DeepResearchStatusEnum(enum.Enum):
    """Status enum for deep research sessions."""
    NOT_STARTED = "NOT_STARTED"
    DECOMPOSING = "DECOMPOSING"
    WAITING_USER_CLARIFICATION = "WAITING_USER_CLARIFICATION"
    WAITING_SCOPE_APPROVAL = "WAITING_SCOPE_APPROVAL"
    RESEARCHING = "RESEARCHING"
    SYNTHESIZING = "SYNTHESIZING"
    WAITING_USER_REVIEW = "WAITING_USER_REVIEW"
    DRILL_DOWN = "DRILL_DOWN"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class HITLStatusEnum(enum.Enum):
    """Human-in-the-loop status enum."""
    NONE = "NONE"
    PENDING = "PENDING"
    RESPONDED = "RESPONDED"
    TIMEOUT = "TIMEOUT"


class DeepResearchSessionModel(Base):
    """
    Model for Deep Research Sessions.

    Each session represents a complex research task that is decomposed into
    parallel sub-tasks executed by independent agents. Supports human-in-the-loop
    checkpoints for clarification, scope approval, and result review.
    """

    __tablename__ = "deep_research_sessions"

    id = Column(Integer, primary_key=True)

    # User and organization
    user_id = Column(String(128), nullable=False)
    org_id = Column(String(128), nullable=True)

    # Link to workbook (optional)
    workbook_id = Column(
        Integer,
        ForeignKey("workbooks.id"),
        nullable=True,
    )

    # Original query and configuration
    original_query = Column(Text, nullable=False)
    research_config = Column(Text, nullable=True)  # JSON string of config

    # Execution status
    status = Column(
        "status",
        Enum(DeepResearchStatusEnum),
        default=DeepResearchStatusEnum.NOT_STARTED,
        nullable=False,
    )
    current_phase = Column(String(50), nullable=True)

    # AWS Step Functions tracking
    step_function_arn = Column(String(512), nullable=True)
    step_function_execution_arn = Column(String(512), nullable=True)

    # Progress tracking
    total_subtasks = Column(Integer, nullable=True, default=0)
    completed_subtasks = Column(Integer, nullable=True, default=0)
    failed_subtasks = Column(Integer, nullable=True, default=0)

    # Human-in-the-loop state
    hitl_status = Column(
        "hitl_status",
        Enum(HITLStatusEnum),
        default=HITLStatusEnum.NONE,
        nullable=False,
    )
    hitl_type = Column(String(50), nullable=True)  # clarification, scope_approval, review
    hitl_questions = Column(Text, nullable=True)  # JSON array of questions
    hitl_responses = Column(Text, nullable=True)  # JSON object of responses
    hitl_task_token = Column(String(1024), nullable=True)  # Step Functions callback token
    hitl_requested_at = Column(DateTime, nullable=True)
    hitl_responded_at = Column(DateTime, nullable=True)

    # Results storage
    final_report_s3_key = Column(String(512), nullable=True)
    executive_summary = Column(Text, nullable=True)
    smart_grid_id = Column(
        Integer,
        ForeignKey("smart_grids.id"),
        nullable=True,
    )

    # Metadata
    total_citations = Column(Integer, nullable=True, default=0)
    average_confidence = Column(Float, nullable=True)
    total_documents_analyzed = Column(Integer, nullable=True, default=0)

    # V2 Architecture Fields (Agentic Units)
    architecture_version = Column(String(10), default="v1")  # "v1" = old DAG, "v2" = agentic units

    # Orchestration state (V2)
    current_iteration = Column(Integer, default=0)  # Plan-Execute-Evaluate cycle count
    max_iterations = Column(Integer, default=10)
    token_budget = Column(Integer, default=100000)
    tokens_used = Column(Integer, default=0)

    # Unit tracking (V2)
    total_units = Column(Integer, default=0)
    completed_units = Column(Integer, default=0)

    # Evaluation state (V2)
    last_evaluation = Column(Text, nullable=True)  # JSON: Last evaluator output
    objective_confidence = Column(Float, nullable=True)  # Overall confidence

    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, nullable=True, default=0)

    # Soft delete and timestamps
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

    # ORM Relationships
    subtasks = relationship(
        "DeepResearchSubTaskModel",
        primaryjoin="and_(DeepResearchSessionModel.id==DeepResearchSubTaskModel.session_id, "
                    "or_(DeepResearchSubTaskModel.is_deleted==False, DeepResearchSubTaskModel.is_deleted==None))",
        order_by="DeepResearchSubTaskModel.sequence_number",
        back_populates="session",
    )

    # V2: Agentic Units relationship
    agentic_units = relationship(
        "DeepResearchAgenticUnitModel",
        primaryjoin="and_(DeepResearchSessionModel.id==DeepResearchAgenticUnitModel.session_id, "
                    "or_(DeepResearchAgenticUnitModel.is_deleted==False, DeepResearchAgenticUnitModel.is_deleted==None))",
        order_by="DeepResearchAgenticUnitModel.wave_number",
        back_populates="session",
    )
