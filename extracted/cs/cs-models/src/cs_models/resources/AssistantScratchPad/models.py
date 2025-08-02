from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean
from ...database import Base


class AssistantScratchPadModel(Base):
    __tablename__ = "assistant_scratchpad"

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey("assistant_sessions.id"),
        nullable=False,
    )
    artifact_id = Column(
        String(128),
        nullable=False,
    )
    source_table = Column(
        String(50),
        nullable=False,
    )
    source_id = Column(
        Integer,
        nullable=False,
    )
    source_details = Column(
        Text,
        nullable=True
    )
    is_deleted = Column(
        Boolean,
        nullable=True
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
