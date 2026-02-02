from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
)
from datetime import datetime

from ...database import Base


class CompanyFilingTypeReviewModel(Base):
    __tablename__ = 'company_filing_type_review'

    id = Column(Integer, primary_key=True)
    company_file_id = Column(
        Integer,
        ForeignKey('company_filings.id'),
        nullable=False,
    )
    filing_type = Column(String(255), nullable=True)
    filing_type_score = Column(Float, nullable=True)
    reviewed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
