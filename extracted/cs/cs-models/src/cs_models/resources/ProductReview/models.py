from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
    Text,
    Boolean,
)

from ...database import Base


class ProductReviewModel(Base):
    __tablename__ = "product_review"

    id = Column(Integer, primary_key=True)
    intervention_norm_id = Column(
        Integer,
        ForeignKey('intervention_norm.id'),
        nullable=False,
    )
    company_sec_id = Column(
        Integer,
        ForeignKey('companies_sec.id'),
        nullable=True,
    )
    company_ous_id = Column(
        Integer,
        ForeignKey('companies_ous.id'),
        nullable=True,
    )
    concern_type = Column(String(50), nullable=False)
    concern_detail = Column(String(128), nullable=False)
    note = Column(Text, nullable=True)
    references = Column(Text, nullable=True)
    assignee_id = Column(
        Integer,
        ForeignKey('assignees.id'),
        nullable=True,
    )
    reviewer_id = Column(
        Integer,
        ForeignKey('reviewers.id'),
        nullable=True,
    )
    reviewed = Column(
        Boolean,
        nullable=True,
    )
    date_logged = Column(DateTime, nullable=False)
    date_reviewed = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
