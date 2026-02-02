from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class NotificationReadStatusModel(Base):
    __tablename__ = 'notifications_read_status'

    id = Column(Integer, primary_key=True)
    notification_id = Column(
        Integer,
        ForeignKey('notifications.id'),
        nullable=False,
    )
    user_id = Column(String(128), nullable=False, index=True)
    seen_at = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
