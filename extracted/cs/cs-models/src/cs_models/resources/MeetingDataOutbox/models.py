from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
)

from ...database import Base


class MeetingDataOutboxModel(Base):
    __tablename__ = "meeting_data_outbox"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(
        Integer,
        ForeignKey('meetings.id'),
        nullable=True,
    )
    meeting_name = Column(String(191), nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    from_website = Column(Boolean, nullable=True)
    meeting_bucket_id = Column(
        Integer,
        ForeignKey('meeting_bucket.id'),
        nullable=True,
    )
    reviewed = Column(Boolean, nullable=True)
    submitted = Column(Boolean, nullable=True)
    submitted_date = Column(DateTime, nullable=True)
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=True,
    )
    error = Column(Text, nullable=True)
    checks = Column(Text, nullable=True)
    completed = Column(Boolean, nullable=True)
    data_entry_type = Column(String(50), nullable=True)
    note = Column(String(128), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
