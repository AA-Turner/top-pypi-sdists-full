from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, Text, Index
from sqlalchemy.orm import relationship
from ...database import Base


class SmartDefGridRunStatus(str, Enum):
    created = "created"
    dispatched = "dispatched"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"
    partial = "partial"   # finished with some failed cells


class SmartDefGridRunScope(str, Enum):
    all = "all"
    empty_only = "empty_only"


class SmartDefGridRunModel(Base):
    __tablename__ = "smart_def_grid_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)  # run_id
    smart_def_grid_id = Column(Integer, ForeignKey("smart_def_grids.id", ondelete="CASCADE"), nullable=False)

    scope_mode = Column(SAEnum(SmartDefGridRunScope), nullable=False, default=SmartDefGridRunScope.all)

    # optional snapshotting to make runs reproducible/debuggable
    outline_json = Column(JSON, nullable=False)  # new outline created for this run
    original_table_json = Column(JSON, nullable=False)    # stamped block at run start
    targets_json = Column(JSON, nullable=True)

    # execution metadata
    status = Column(
        SAEnum(
            SmartDefGridRunStatus,
            validate_strings=True,  # allow assigning "created" etc. as strings too
        ),
        nullable=False,
        default=SmartDefGridRunStatus.created,
    )

    started_by_user_id = Column(String(64), nullable=False)
    notes = Column(Text, nullable=True)
    # optional idempotency token if you want “re-run latest”
    client_token = Column(String(128), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    grid = relationship("SmartDefGridModel", backref="runs")
    __table_args__ = (
        Index("ix_sdgr_runs_grid_created", "smart_def_grid_id", "created_at"),
    )
