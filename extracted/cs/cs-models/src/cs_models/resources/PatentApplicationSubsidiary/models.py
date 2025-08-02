from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)

from ...database import Base


class PatentApplicationSubsidiaryModel(Base):
    __tablename__ = "patent_application_subsidiaries"

    id = Column(Integer, primary_key=True)
    patent_application_id = Column(
        Integer,
        ForeignKey('patent_applications.id'),
        nullable=False,
    )
    subsidiary_id = Column(
        Integer,
        ForeignKey('subsidiaries.id'),
        nullable=False,
    )
    score = Column(
        Float,
        nullable=False,
    )
    published_date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
