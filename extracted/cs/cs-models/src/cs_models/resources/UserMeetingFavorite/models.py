from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from datetime import datetime

from ...database import Base


class UserMeetingFavoriteModel(Base):
    __tablename__ = 'user_meeting_favorite'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    meeting_id = Column(
        Integer,
        ForeignKey('meetings.id'),
        nullable=False,
    )
    pubmed_id = Column(
        Integer,
        ForeignKey('pubmed.id'),
        nullable=False,
    )
    favorite_status = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
