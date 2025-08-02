from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
)

from ...database import Base


class ViewPublicationTargetModel(Base):
    __tablename__ = "_view_publication_targets"

    id = Column(Integer, primary_key=True)
    target_id = Column(
        Integer,
        ForeignKey('targets.id'),
        nullable=False,
    )
    date = Column(DateTime, nullable=False)
    table_name = Column(String(50), nullable=False)
    table_id = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
