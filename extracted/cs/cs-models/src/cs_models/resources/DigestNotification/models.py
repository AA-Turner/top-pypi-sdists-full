from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from ...database import Base


class DigestNotificationModel(Base):
    __tablename__ = "digest_notifications"

    id = Column(Integer, primary_key=True)
    digest_id = Column(
        Integer,
        ForeignKey('digests.id'),
        nullable=False,
    )
    notification_id = Column(
        Integer,
        ForeignKey('notifications.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
