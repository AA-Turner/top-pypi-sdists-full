from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, Boolean, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from ...database import Base


class SmartDefGridCellModel(Base):
    """
    One logical 'master' cell from the outline; the cell_id is stable.
    Header cells exist too (is_header), in case you later want header questions.
    """
    __tablename__ = "smart_def_grid_cells"

    # Composite natural key (table_id, cell_id)
    smart_def_grid_id = Column(Integer, ForeignKey("smart_def_grids.id", ondelete="CASCADE"), primary_key=True)
    cell_id = Column(String(36), primary_key=True)  # stable UUID you generated

    # Positional metadata + spans help future reflow/debug, not needed at runtime for writeback
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    row_span = Column(Integer, nullable=False, default=1)
    col_span = Column(Integer, nullable=False, default=1)
    is_header = Column(Boolean, nullable=False, default=False)

    header_path_row = Column(JSON, nullable=False, default=list)  # ["Efficacy (vs PBO)", "Clinical Remission"]
    header_path_col = Column(JSON, nullable=False, default=list)  # ["Humira"] etc.

    # Formatting guidance to apply when writing display strings
    formatting_spec = Column(JSON, nullable=True)

    # Optional: cache of the latest generated question id
    latest_question_id = Column(Integer, ForeignKey("smart_def_grid_cell_questions.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    table = relationship("SmartDefGridModel", back_populates="cells")
    latest_question = relationship("SmartDefGridCellQuestionModel", foreign_keys=[latest_question_id], uselist=False)

    # Canonical applied cell value (write-back)
    applied_value = relationship(
        "SmartDefGridCellValueModel",
        back_populates="cell",
        uselist=False,
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("smart_def_grid_id", "row", "col", name="uq_sdg_cell_pos"),
        Index("ix_smart_def_grid_cells_header", "smart_def_grid_id", "is_header"),
    )
