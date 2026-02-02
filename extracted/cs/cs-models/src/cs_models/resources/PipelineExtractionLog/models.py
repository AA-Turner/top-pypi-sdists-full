from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum,
)
from datetime import datetime

from ...database import Base


class PipelineExtractionLogModel(Base):
    __tablename__ = 'pipeline_extraction_logs'

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey('pipeline_crawl_sessions.id'),
        nullable=False,
        index=True,
    )
    page_id = Column(
        Integer,
        ForeignKey('pipeline_crawled_pages.id'),
        nullable=True,
    )

    # Log details (MySQL ENUM)
    log_level = Column(
        Enum('debug', 'info', 'warning', 'error'),
        nullable=False,
        default='info',
        index=True,
    )
    message = Column(Text, nullable=False)

    # Context
    extraction_method = Column(String(50), nullable=True)
    model_name = Column(String(128), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    api_latency_ms = Column(Integer, nullable=True)

    # Error tracking
    exception_type = Column(String(256), nullable=True)
    exception_message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)

    # Retry tracking
    attempt_number = Column(Integer, nullable=True, default=1)
    max_attempts = Column(Integer, nullable=True, default=3)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
