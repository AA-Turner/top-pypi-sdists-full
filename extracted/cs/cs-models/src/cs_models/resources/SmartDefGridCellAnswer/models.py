from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Float, String, JSON, Integer, Index, Text, BigInteger, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from ...database import Base


class SmartDefGridCellAnswerModel(Base):
    """
    Answers emitted by workers. Keep multiple rows per question (retries, models).
    """
    __tablename__ = "smart_def_grid_cell_answers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("smart_def_grid_cell_questions.id", ondelete="CASCADE"), nullable=False)

    smart_def_grid_id = Column(Integer, ForeignKey("smart_def_grids.id", ondelete="CASCADE"), nullable=False)
    run_id = Column(Integer, ForeignKey("smart_def_grid_runs.id", ondelete="SET NULL"), nullable=True)
    cell_id = Column(String(36), nullable=False)

    # canonical payload
    raw_value = Column(Float, nullable=True)        # numeric scalar (if any)
    text_value = Column(Text, nullable=True)        # string/summary
    display_text = Column(Text, nullable=True)      # preformatted; writeback may still reformat
    citations = Column(JSON, nullable=True)         # list of {url|doi|title|snippet|...}
    extra_payload = Column(JSON, nullable=True)     # any provider-specific structure

    # provenance
    provider = Column(String(64), nullable=True)    # e.g., "gpt-4.1"
    provider_meta = Column(JSON, nullable=True)     # tokens, latency, etc.

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # convenience index to quickly get latest by created_at
    __table_args__ = (
        ForeignKeyConstraint(
            ["smart_def_grid_id", "cell_id"],
            ["smart_def_grid_cells.smart_def_grid_id", "smart_def_grid_cells.cell_id"],
            ondelete="CASCADE",
        ),
        Index("ix_smart_def_grid_cell_answers_cell", "smart_def_grid_id", "cell_id", "created_at"),
        Index("ix_sdgca_run_cell", "run_id", "smart_def_grid_id", "cell_id", "created_at"),
    )

    question = relationship("SmartDefGridCellQuestionModel", back_populates="answers")
    run = relationship("SmartDefGridRunModel")
