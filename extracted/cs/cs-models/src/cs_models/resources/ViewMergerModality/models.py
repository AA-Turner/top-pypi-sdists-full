from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
)

from ...database import Base


class ViewMergerModalityModel(Base):
    __tablename__ = "_view_merger_modalities"

    id = Column(Integer, primary_key=True)
    merger_id = Column(
        Integer,
        ForeignKey('mergers.id'),
        nullable=False,
    )
    modality = Column(
        String(191),
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
