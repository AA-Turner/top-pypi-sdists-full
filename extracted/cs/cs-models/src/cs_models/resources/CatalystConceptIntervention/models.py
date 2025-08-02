from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
)

from ...database import Base


class CatalystConceptInterventionModel(Base):
    __tablename__ = "catalyst_concepts_interventions"

    id = Column(Integer, primary_key=True)
    catalyst_concept_id = Column(
        Integer,
        ForeignKey('catalyst_concepts.id'),
        nullable=False,
    )
    intervention_id = Column(
        Integer,
        ForeignKey('interventions.id'),
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
