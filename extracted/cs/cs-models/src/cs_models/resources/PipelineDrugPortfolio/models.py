from sqlalchemy import (
    Column,
    BIGINT,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    Boolean,
    ForeignKey,
    Enum,
    Index,
    JSON,
)
from datetime import datetime

from ...database import Base


class PipelineDrugPortfolioModel(Base):
    __tablename__ = 'pipeline_drug_portfolio'

    id = Column(BIGINT, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey('pipeline_crawl_sessions.id'),
        nullable=False,
        index=True,
    )
    page_id = Column(
        Integer,
        ForeignKey('pipeline_crawled_pages.id'),
        nullable=False,
        index=True,
    )

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

    # Core drug information
    drug_name = Column(String(512), nullable=False, index=True)
    drug_name_normalized = Column(String(512), nullable=True, index=True)
    synonyms = Column(JSON, nullable=True)

    modality = Column(String(256), nullable=True)
    targets = Column(JSON, nullable=True)
    mechanism_of_action = Column(Text, nullable=True)

    # Indications (JSON)
    indications = Column(JSON, nullable=False)

    # Additional information (JSON)
    additional_info = Column(JSON, nullable=True)

    # Extraction metadata (MySQL ENUM)
    extraction_method = Column(
        Enum('html_parsing', 'vision_model', 'hybrid', 'manual'),
        nullable=False,
    )
    extraction_confidence = Column(Float, nullable=True)
    raw_extraction_text = Column(Text, nullable=True)

    # Data quality flags
    is_verified = Column(Boolean, nullable=True, default=False)
    is_duplicate = Column(Boolean, nullable=True, default=False, index=True)
    needs_review = Column(Boolean, nullable=True, default=False, index=True)
    review_notes = Column(Text, nullable=True)

    # Timestamps
    extracted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        Index('idx_company_drug_name', 'company_sec_id', 'drug_name_normalized'),
        Index('idx_session_drug', 'session_id', 'drug_name_normalized'),
    )
