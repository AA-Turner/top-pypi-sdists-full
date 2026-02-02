from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Boolean,
    String,
)

from ...database import Base


class InterventionNormNoteLinkModel(Base):
    __tablename__ = "intervention_norm_notes_links"

    id = Column(Integer, primary_key=True)
    norm_cui = Column(String(191), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    is_external = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
