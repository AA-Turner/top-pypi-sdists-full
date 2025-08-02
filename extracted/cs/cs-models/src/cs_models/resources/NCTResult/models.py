from sqlalchemy import (
    Integer,
    Column,
    DateTime,
    Text,
    ForeignKey,
)
from datetime import datetime
from ...database import Base


class NCTResultModel(Base):
    __tablename__ = "nct_results"

    id = Column(Integer, primary_key=True)
    nct_study_id = Column(
        Integer,
        ForeignKey('nct_study.id'),
        nullable=False,
    )
    results = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
