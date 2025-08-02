from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Float,
    Boolean,
)

from ...database import Base


class FDADrugReviewFileConditionModel(Base):
    __tablename__ = "fda_drug_review_files_conditions"

    id = Column(Integer, primary_key=True)
    fda_drug_review_file_id = Column(
        Integer,
        ForeignKey('fda_drug_review_files.id'),
        nullable=False,
    )
    condition_id = Column(
        Integer,
        ForeignKey('conditions.id'),
        nullable=False,
    )
    score = Column(
        Float,
        nullable=False,
    )
    preferred = Column(Boolean, nullable=True)
    data_readout = Column(Boolean, nullable=True)
    date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
