from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    String,
    Text,
)
from datetime import datetime

from ...database import Base


class EventsQueueModel(Base):
    __tablename__ = 'events_queue'

    id = Column(Integer, primary_key=True)
    artifact_id = Column(String(50), nullable=False)
    processed = Column(
        Boolean,
        nullable=True,
    )
    attempts = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    submitted = Column(Boolean, nullable=True)
    submitted_date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
