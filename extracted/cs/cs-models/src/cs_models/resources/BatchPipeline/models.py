from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)

from ...database import Base


class BatchPipelineModel(Base):
    __tablename__ = "batch_pipeline"

    id = Column(Integer, primary_key=True)
    index_name = Column(String(128), nullable=False, index=True)
    pipeline = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        index=True,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
