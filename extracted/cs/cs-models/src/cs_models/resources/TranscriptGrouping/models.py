from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class TranscriptGroupingModel(Base):
    __tablename__ = 'transcripts_grouping'

    id = Column(Integer, primary_key=True)
    grouping_id = Column(Integer, nullable=False, index=True)
    grouping_name = Column(String(191), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
