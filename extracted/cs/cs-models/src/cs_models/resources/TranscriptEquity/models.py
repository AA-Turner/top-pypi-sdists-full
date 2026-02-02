from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class TranscriptEquityModel(Base):
    __tablename__ = 'transcripts_equities'

    id = Column(Integer, primary_key=True)
    transcript_id = Column(
        Integer,
        ForeignKey('transcripts.id'),
        nullable=False,
    )
    equity_id = Column(Integer, index=True, nullable=False)
    date = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
