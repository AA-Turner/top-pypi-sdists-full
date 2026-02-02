from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    ForeignKey,
    Enum,
)
from datetime import datetime

from ...database import Base


class PipelineCrawlSessionModel(Base):
    __tablename__ = 'pipeline_crawl_sessions'

    id = Column(Integer, primary_key=True)
    company_sec_id = Column(
        Integer,
        ForeignKey('companies_sec.id'),
        nullable=True,
        index=True,
    )
    company_ous_id = Column(
        Integer,
        ForeignKey('companies_ous.id'),
        nullable=True,
        index=True,
    )

    # Session tracking
    session_uuid = Column(String(36), nullable=False, unique=True, index=True)
    crawl_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Timing metrics
    crawl_duration_seconds = Column(Float, nullable=True)
    page_discovery_time_seconds = Column(Float, nullable=True)
    extraction_time_seconds = Column(Float, nullable=True)

    # Status tracking (MySQL ENUM)
    status = Column(
        Enum('started', 'discovering_pages', 'extracting_data', 'completed', 'failed', 'timeout'),
        nullable=False,
        default='started',
        index=True,
    )
    error_message = Column(Text, nullable=True)

    # Crawl statistics
    total_pages_discovered = Column(Integer, nullable=True, default=0)
    total_pages_crawled = Column(Integer, nullable=True, default=0)
    total_screenshots_captured = Column(Integer, nullable=True, default=0)
    total_drugs_extracted = Column(Integer, nullable=True, default=0)

    # Crawl configuration
    crawl_method = Column(String(50), nullable=True)
    max_depth = Column(Integer, nullable=True, default=2)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
