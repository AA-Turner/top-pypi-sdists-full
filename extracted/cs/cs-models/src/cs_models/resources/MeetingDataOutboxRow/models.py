from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Text,
)

from ...database import Base


class MeetingDataOutboxRowModel(Base):
    __tablename__ = "meeting_data_outbox_rows"

    id = Column(Integer, primary_key=True)
    meeting_data_outbox_id = Column(
        Integer,
        ForeignKey('meeting_data_outbox.id'),
        nullable=False,
    )
    row = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
