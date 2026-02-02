from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
)

from ...database import Base


class MergerActionRecordModel(Base):
    __tablename__ = "merger_action_records"

    id = Column(Integer, primary_key=True)
    merger_action_id = Column(
        Integer,
        ForeignKey('merger_actions.id'),
        nullable=False,
    )
    table = Column(String(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
