from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class SellSideAbstractMentionModel(Base):
    __tablename__ = "sell_side_abstract_mentions"

    id = Column(Integer, primary_key=True)

    # which PDF / note
    user_document_id = Column(
        Integer,
        ForeignKey("user_documents.id"),
        nullable=False,
        index=True,
    )

    # which conference
    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id"),
        nullable=False,
        index=True,
    )

    # optional locator
    page_number = Column(Integer, nullable=True)

    # raw LLM fields
    title = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    abstract_number = Column(String(64), nullable=True)
    abstract_search_query = Column(Text, nullable=True)
    context = Column(Text, nullable=True)
    sentiment = Column(Text, nullable=True)
    llm_confidence = Column(Float, nullable=True)

    raw_json = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
        nullable=False,
    )

