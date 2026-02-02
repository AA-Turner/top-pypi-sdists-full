from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class TranscriptGroupingMapModel(Base):
    __tablename__ = 'transcripts_grouping_map'

    id = Column(Integer, primary_key=True)
    transcript_id = Column(
        Integer,
        ForeignKey('transcripts.id'),
        nullable=False,
    )
    grouping_id = Column(
        Integer,
        ForeignKey('transcripts_grouping.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
