from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
)

from ...database import Base


class EventLLMModel(Base):
    __tablename__ = "events_llm"

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    event_type = Column(String(128), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    news_id = Column(
        Integer,
        ForeignKey('newswires.id'),
        nullable=True,
    )
    sec_filing_id = Column(
        Integer,
        ForeignKey('companies_sec_filings.id'),
        nullable=True,
    )
    reference_text = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
