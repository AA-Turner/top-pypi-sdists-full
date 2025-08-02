from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class UserSavedSearchAccessModel(Base):
    __tablename__ = 'user_saved_searches_access'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    saved_search_id = Column(
        Integer,
        ForeignKey('user_saved_searches.id'),
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=True)
    instant_notification = Column(Boolean, nullable=True)
    daily_digest = Column(Boolean, nullable=True)
    weekly_digest = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
