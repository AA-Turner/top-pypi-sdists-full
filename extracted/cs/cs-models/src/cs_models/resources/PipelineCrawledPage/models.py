from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    Enum,
    Index,
    UniqueConstraint,
)
from datetime import datetime

from ...database import Base


class PipelineCrawledPageModel(Base):
    __tablename__ = 'pipeline_crawled_pages'

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey('pipeline_crawl_sessions.id'),
        nullable=False,
        index=True,
    )

    # URL information
    url = Column(String(1024), nullable=False)
    url_hash = Column(String(64), nullable=False, index=True)
    page_title = Column(String(512), nullable=True)

    # Page content storage (S3)
    html_content_s3_key = Column(String(512), nullable=True)
    html_content_hash = Column(String(64), nullable=True)
    html_content_length = Column(Integer, nullable=True)

    # Screenshot storage (S3)
    screenshot_s3_key = Column(String(512), nullable=True)
    screenshot_hash = Column(String(64), nullable=True)
    screenshot_width = Column(Integer, nullable=True)
    screenshot_height = Column(Integer, nullable=True)
    screenshot_file_size = Column(Integer, nullable=True)

    # Page classification (MySQL ENUM)
    page_type = Column(
        Enum('pipeline', 'science', 'rd', 'products', 'clinical_trials', 'other'),
        nullable=True,
    )
    relevance_score = Column(Float, nullable=True)

    # Extraction metadata
    has_drug_data = Column(Boolean, nullable=True, default=False)
    extraction_method = Column(String(50), nullable=True)

    # Crawl metadata
    crawl_depth = Column(Integer, nullable=True, default=0)
    parent_page_id = Column(Integer, ForeignKey('pipeline_crawled_pages.id'), nullable=True)
    discovered_from_url = Column(String(1024), nullable=True)

    # Technical metadata
    http_status_code = Column(Integer, nullable=True)
    content_type = Column(String(128), nullable=True)
    response_time_ms = Column(Integer, nullable=True)

    # Timestamps
    crawled_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        Index('idx_session_url_hash', 'session_id', 'url_hash'),
        UniqueConstraint('session_id', 'url_hash', name='uq_session_url'),
    )
