from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from datetime import datetime

from ...database import Base


class PubmedMeetingSellSideSignalModel(Base):
    __tablename__ = "pubmed_meeting_sell_side_signals"

    id = Column(Integer, primary_key=True)

    pubmed_id = Column(
        Integer,
        ForeignKey("pubmed.id"),
        nullable=False,
        index=True,
    )
    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id"),
        nullable=False,
        index=True,
    )
    sell_side_source_id = Column(
        Integer,
        ForeignKey("sell_side_sources.id"),
        nullable=False,
        index=True,
    )

    # intensity
    doc_count = Column(Integer, nullable=False)      # distinct notes
    mention_count = Column(Integer, nullable=False)  # total mentions across those notes

    # sentiment summary
    avg_sentiment = Column(Float, nullable=True)
    max_sentiment = Column(Float, nullable=True)

    first_mention_at = Column(DateTime, nullable=True)
    last_mention_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "pubmed_id",
            "meeting_id",
            "sell_side_source_id",
            name="uq_pubmed_meeting_source",
        ),
    )
