from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
    ForeignKey,
)

from ...database import Base


class BatchJobStatusModel(Base):
    __tablename__ = "batch_jobs_status"

    id = Column(Integer, primary_key=True)
    pipeline_id = Column(
        Integer,
        ForeignKey("batch_pipeline.id"),
        nullable=False,
    )
    job_id = Column(String(128), nullable=False, index=True)
    job_def = Column(String(128), nullable=False, index=True)
    job_queue = Column(String(125), nullable=False, index=True)
    parameters = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)
    reason = Column(String(50), nullable=True)
    exit_code = Column(String(20), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        index=True,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
