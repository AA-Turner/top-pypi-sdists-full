from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    DECIMAL,
)
from datetime import datetime

from ...database import Base


class CompanyOUSModel(Base):
    __tablename__ = 'companies_ous'

    id = Column(Integer, primary_key=True)
    cik = Column(Integer, index=True, nullable=True)
    name = Column(String(190), unique=True, nullable=False)
    ticker = Column(String(20), nullable=True, index=True)
    exchange = Column(String(100), nullable=True)
    market_cap = Column(DECIMAL(20, 2), nullable=False)
    company_url = Column(String(255), nullable=True)
    pipeline_url = Column(String(255), nullable=True)
    ir_url = Column(String(255), nullable=True)
    is_activated = Column(Boolean, nullable=True)
    is_searchable = Column(Boolean, nullable=True)
    last_crawl_date = Column(DateTime, nullable=True)
    last_pipeline_crawl_date = Column(DateTime, nullable=True)
    pipeline_crawl_enabled = Column(Boolean, nullable=True, default=True)
    industry_type = Column(String(50), nullable=True)
    company_sec_link = Column(
        Integer,
        ForeignKey('companies_sec.id'),
        nullable=True,
    )
    relevant_links = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
