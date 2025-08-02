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


class LicensingCollabConditionModel(Base):
    __tablename__ = "licensing_collab_conditions"

    id = Column(Integer, primary_key=True)
    licensing_collab_id = Column(
        Integer,
        ForeignKey('licensing_collab.id'),
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
    selected = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
