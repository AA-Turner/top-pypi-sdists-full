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


class FDADrugReviewFileModel(Base):
    __tablename__ = 'fda_drug_review_files'

    id = Column(Integer, primary_key=True)
    fda_drug_review_id = Column(
        Integer,
        ForeignKey('fda_drug_reviews.id'),
        nullable=False,
    )
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=False,
    )
    date = Column(DateTime, nullable=True)
    title = Column(String(255), nullable=True)
    page_count = Column(Integer, nullable=True)
    type = Column(String(255), nullable=True)
    orig_file_url = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    unprocessed = Column(Boolean, nullable=True)
    reviewed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
