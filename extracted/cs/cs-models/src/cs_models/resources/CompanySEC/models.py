from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    Boolean,
    Text,
    DECIMAL,
)
from datetime import datetime

from ...database import Base


class CompanySECModel(Base):
    __tablename__ = 'companies_sec'

    id = Column(Integer, primary_key=True)
    lead_company = Column(Boolean, nullable=True)
    cik_str = Column(String(128), nullable=False)
    ticker = Column(String(20), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    exchange = Column(String(50), nullable=True)
    market_cap = Column(DECIMAL(20, 2), nullable=False)
    company_url = Column(String(255), nullable=True)
    pipeline_url = Column(String(255), nullable=True)
    ir_url = Column(String(255), nullable=True)
    is_activated = Column(Boolean, nullable=True)
    is_biopharma = Column(Boolean, nullable=True)
    is_searchable = Column(Boolean, nullable=True)
    discarded = Column(Boolean, nullable=True)
    skip_sec = Column(Boolean, nullable=True)
    last_crawl_date = Column(DateTime, nullable=True)
    last_pipeline_crawl_date = Column(DateTime, nullable=True)
    pipeline_crawl_enabled = Column(Boolean, nullable=True, default=True)
    industry_type = Column(String(50), nullable=True)
    relevant_links = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (UniqueConstraint('cik_str', 'ticker'),)
