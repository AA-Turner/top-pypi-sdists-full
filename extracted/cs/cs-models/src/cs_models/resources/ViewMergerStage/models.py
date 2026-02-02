from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from ...database import Base


class ViewMergerStageModel(Base):
    __tablename__ = "_view_merger_stages"

    id = Column(Integer, primary_key=True)
    merger_id = Column(
        Integer,
        ForeignKey('mergers.id'),
        nullable=False,
    )
    stage = Column(
        Integer,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
