from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    ForeignKey,
)

from ...database import Base


class NCTSubsidiaryModel(Base):
    __tablename__ = "nct_subsidiaries"

    id = Column(Integer, primary_key=True)
    nct_id = Column(String(128), nullable=False, index=True)
    nct_study_id = Column(
        Integer,
        ForeignKey('nct_study.id'),
        nullable=False,
    )
    subsidiary_id = Column(
        Integer,
        ForeignKey('subsidiaries.id'),
        nullable=False,
    )
    lead_or_collaborator = Column(String(50))
    study_start_date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    __table_args__ = (UniqueConstraint("nct_study_id", "subsidiary_id"),)
