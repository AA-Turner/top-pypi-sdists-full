from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    String,
    Text,
)

from ...database import Base


class ArtifactVectorIndexQueueModel(Base):
    __tablename__ = "artifact_vector_index_queue"

    id = Column(Integer, primary_key=True)
    artifact_id = Column(
        String(50),
        nullable=False,
        index=True,
    )
    attempts = Column(Integer, nullable=True)
    submitted = Column(Boolean, nullable=True)
    submitted_date = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
