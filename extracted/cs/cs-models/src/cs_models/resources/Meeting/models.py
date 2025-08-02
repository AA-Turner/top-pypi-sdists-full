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


class MeetingModel(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    meeting_name = Column(String(191), nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    title_release_date = Column(DateTime, nullable=True)
    abstract_release_date = Column(DateTime, nullable=True)
    from_website = Column(Boolean, nullable=True)
    meeting_bucket_id = Column(
        Integer,
        ForeignKey('meeting_bucket.id'),
        nullable=True,
    )
    author_pipeline = Column(Boolean, nullable=True)
    insights_pipeline = Column(Boolean, nullable=True)
    important_dates = Column(Text, nullable=True)
    indexing_status = Column(String(128), nullable=True)
    status = Column(String, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
