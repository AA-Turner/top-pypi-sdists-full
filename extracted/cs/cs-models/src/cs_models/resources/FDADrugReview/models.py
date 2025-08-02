from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class FDADrugReviewModel(Base):
    __tablename__ = 'fda_drug_reviews'

    id = Column(Integer, primary_key=True)
    application_docs_id = Column(String(128), nullable=False)
    application_docs_type_id = Column(Integer, nullable=False)
    appl_no = Column(String(50), nullable=False)
    submission_type = Column(String(50), nullable=True)
    submission_no = Column(String(50), nullable=True)
    application_doc_url = Column(String(255), nullable=True)
    application_doc_date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
