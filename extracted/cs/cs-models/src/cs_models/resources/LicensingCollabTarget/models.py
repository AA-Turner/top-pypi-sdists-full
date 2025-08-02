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


class LicensingCollabTargetModel(Base):
    __tablename__ = "licensing_collab_targets"

    id = Column(Integer, primary_key=True)
    licensing_collab_id = Column(
        Integer,
        ForeignKey('licensing_collab.id'),
        nullable=False,
    )
    target_id = Column(
        Integer,
        ForeignKey('targets.id'),
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
