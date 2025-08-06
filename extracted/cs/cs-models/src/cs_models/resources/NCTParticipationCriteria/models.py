from sqlalchemy import (
    Integer,
    Column,
    DateTime,
    ForeignKey,
    Text,
)
from datetime import datetime
from ...database import Base


class NCTParticipationCriteriaModel(Base):
    __tablename__ = "nct_participation_criteria"

    id = Column(Integer, primary_key=True)
    nct_study_id = Column(
        Integer,
        ForeignKey('nct_study.id'),
        nullable=False,
    )
    participation_criteria = Column(Text)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
