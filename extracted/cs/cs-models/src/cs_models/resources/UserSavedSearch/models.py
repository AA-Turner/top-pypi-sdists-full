from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
)
from datetime import datetime

from ...database import Base


class UserSavedSearchModel(Base):
    __tablename__ = 'user_saved_searches'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    search_name = Column(String(128), nullable=False)
    search_query = Column(Text, nullable=False)
    search_type = Column(String(128), nullable=False)
    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=False)
    last_processed = Column(DateTime, nullable=True)
    instant_notification = Column(Boolean, nullable=True)
    daily_digest = Column(Boolean, nullable=True)
    weekly_digest = Column(Boolean, nullable=True)
    questions = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
