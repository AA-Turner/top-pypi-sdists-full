from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
)
from datetime import datetime

from ...database import Base


class TranscriptModel(Base):
    __tablename__ = 'transcripts'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    title = Column(String(191), nullable=False)
    event_type = Column(String(50), nullable=True)
    event_tags = Column(Text, nullable=True)
    human_verified = Column(Boolean, nullable=True)
    transcription_status = Column(String(50), nullable=True)
    audio_url = Column(String(191), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
