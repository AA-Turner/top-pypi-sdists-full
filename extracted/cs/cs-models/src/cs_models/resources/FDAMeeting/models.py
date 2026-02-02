from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)
from datetime import datetime
from ...database import Base


class FDAMeetinglModel(Base):
    __tablename__ = 'fda_meetings'

    id = Column(Integer, primary_key=True)
    meeting_type = Column(String(128), nullable=False)
    meeting_name = Column(String(256), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    center = Column(String(128), nullable=True)
    agenda = Column(Text, nullable=True)
    meeting_link = Column(String(255), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
