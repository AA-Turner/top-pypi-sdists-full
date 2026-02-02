"""Models for Deep Research Agentic Units - Self-contained research modules."""
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


class UnitStatusEnum(enum.Enum):
    """Status enum for agentic units."""
    PENDING = "PENDING"
    PLANNING = "PLANNING"       # Internal DAG being planned
    EXECUTING = "EXECUTING"     # Internal tasks running
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class DeepResearchAgenticUnitModel(Base):
    """
    Model for Deep Research Agentic Units.

    An Agentic Unit is a self-contained research module that answers
    ONE coherent objective using any combination of internal tasks
    (DISCOVERY, INVESTIGATION, SMART_GRID, AGGREGATION).

    Part of the V2 architecture that replaces rigid upfront DAG decomposition
    with an adaptive Plan -> Execute -> Evaluate loop.
    """

    __tablename__ = "deep_research_agentic_units"

    id = Column(Integer, primary_key=True)

    # Parent session
    session_id = Column(
        Integer,
        ForeignKey("deep_research_sessions.id"),
        nullable=False,
    )

    # Identity
    unit_id = Column(String(50), nullable=False)  # Logical ID: "A", "B", "C", etc.
    unit_label = Column(String(255), nullable=True)  # Human-readable label
    objective = Column(Text, nullable=False)  # What this unit answers

    # DAG Structure (outer DAG - dependencies between units)
    depends_on = Column(Text, nullable=True)  # JSON: ["A", "B"] - other unit_ids
    wave_number = Column(Integer, default=0)  # Computed from dependencies

    # Internal Structure (inner DAG - tasks within this unit)
    internal_dag = Column(Text, nullable=True)  # JSON: List of internal tasks
    internal_dag_planned = Column(Boolean, default=False)

    # Execution State
    status = Column(
        "status",
        Enum(UnitStatusEnum),
        default=UnitStatusEnum.PENDING,
        nullable=False,
    )

    # Outputs (populated after execution)
    result_s3_key = Column(String(512), nullable=True)
    result_summary = Column(Text, nullable=True)  # Concise answer to objective
    entities_discovered = Column(Text, nullable=True)  # JSON: Entities found (if any)
    confidence = Column(Float, nullable=True)  # 0-1 confidence in results
    gaps_identified = Column(Text, nullable=True)  # JSON: What couldn't be answered

    # Metrics
    tokens_used = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    tasks_failed = Column(Integer, default=0)

    # Context from dependencies (populated before execution)
    input_context = Column(Text, nullable=True)  # JSON: Summaries from dependency units

    # Timestamps
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    # Soft delete
    is_deleted = Column(Boolean, nullable=True)

    # ORM Relationships
    session = relationship(
        "DeepResearchSessionModel",
        back_populates="agentic_units",
    )

    internal_tasks = relationship(
        "DeepResearchSubTaskModel",
        primaryjoin="and_(DeepResearchAgenticUnitModel.id==DeepResearchSubTaskModel.agentic_unit_id, "
                    "or_(DeepResearchSubTaskModel.is_deleted==False, DeepResearchSubTaskModel.is_deleted==None))",
        back_populates="agentic_unit",
    )
