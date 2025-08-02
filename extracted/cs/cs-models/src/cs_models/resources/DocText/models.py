from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    Boolean,
)

from ...database import Base


class DocTextModel(Base):
    __tablename__ = "doc_texts"

    id = Column(Integer, primary_key=True)
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
    company_filing_id = Column(
        Integer,
        ForeignKey('company_filings.id'),
        nullable=True,
    )
    fda_meeting_filing_id = Column(
        Integer,
        ForeignKey('fda_meeting_filings.id'),
        nullable=True,
    )
    pubmed_id = Column(
        Integer,
        ForeignKey('pubmed.id'),
        nullable=True,
    )
    text_type = Column(String(20), nullable=True)
    text = Column(Text, nullable=False)
    preferred = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
