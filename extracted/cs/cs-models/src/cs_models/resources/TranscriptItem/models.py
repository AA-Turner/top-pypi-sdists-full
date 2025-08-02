from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class TranscriptItemModel(Base):
    __tablename__ = 'transcript_items'

    id = Column(Integer, primary_key=True)
    transcript_item_id = Column(Integer, nullable=False, index=True)
    transcript_id = Column(
        Integer,
        ForeignKey('transcripts.id'),
        nullable=False,
    )
    transcript = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=True)
    speaker_id = Column(Integer, nullable=True)
    speaker_name = Column(String(128), nullable=True)
    speaker_title = Column(String(128), nullable=True)
    audio_url = Column(String(191), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
