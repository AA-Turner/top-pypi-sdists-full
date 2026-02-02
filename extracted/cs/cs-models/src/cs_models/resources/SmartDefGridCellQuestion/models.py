import enum
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, Boolean, Index, Text, Enum, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from ...database import Base


class QuestionStatus(str, enum.Enum):
    pending = "pending"     # created, not enqueued yet
    queued = "queued"      # sent to your queue
    running = "running"     # worker picked it up
    succeeded = "succeeded"   # at least one answer persisted
    failed = "failed"      # irrecoverable error (manual retry/override)
    cancelled = "cancelled"  # cancelled


class ExpectedType(str, enum.Enum):
    number = "number"
    text = "text"


class SmartDefGridCellQuestionModel(Base):
    """
    One question per cell (you may create new ones on re-ask/revision).
    """
    __tablename__ = "smart_def_grid_cell_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)  # question_id (uuid)
    smart_def_grid_id = Column(Integer, ForeignKey("smart_def_grids.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(Integer, ForeignKey("smart_def_grid_runs.id", ondelete="SET NULL"), nullable=True)
    cell_id = Column(String(36), nullable=False)

    question_text = Column(Text, nullable=False)
    expected_type = Column(Enum(ExpectedType), nullable=False)
    must_cite = Column(Boolean, nullable=False, default=True)

    topic_key = Column(JSON, nullable=True)
    retrieval_hints = Column(JSON, nullable=True)

    # Answer
    answer_text = Column(Text, nullable=True)
    answer_info = Column(JSON, nullable=True)

    # Queue & lifecycle
    status = Column(Enum(QuestionStatus), nullable=False, default=QuestionStatus.pending)
    priority = Column(Integer, nullable=False, default=5)     # lower = higher priority
    attempts = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)

    idempotency_key = Column(String(64), nullable=True)       # to avoid dup work
    dedupe_hash = Column(String(64), nullable=True)           # e.g., hash(table_id, cell_id, question_text)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    # relationships
    answers = relationship("SmartDefGridCellAnswerModel", back_populates="question", cascade="all, delete-orphan")
    run = relationship("SmartDefGridRunModel")

    __table_args__ = (
        # Useful to grab next jobs: status+priority+created
        Index("ix_smart_def_grid_cell_questions_queue", "status", "priority", "created_at"),
        # Quick lookup for this cell's active question(s)
        Index("ix_smart_def_grid_cell_questions_cell", "smart_def_grid_id", "cell_id"),
        Index("ix_sdgcq_run_status", "run_id", "status", "priority", "created_at"),
        Index("ix_sdgcq_run_cell", "run_id", "smart_def_grid_id", "cell_id"),
        ForeignKeyConstraint(
            ["smart_def_grid_id", "cell_id"],
            ["smart_def_grid_cells.smart_def_grid_id", "smart_def_grid_cells.cell_id"],
            ondelete="CASCADE",
        ),
        # strong uniqueness if you want only one ACTIVE per cell; or enforce app-side
        # UniqueConstraint("table_id", "cell_id", "status", name="uq_cell_question_cell_status"),
    )
