from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
)

from ...database import Base


class UserActivityModel(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    page = Column(String(50), nullable=False, index=True)
    endpoint = Column(String(128), nullable=False)
    payload = Column(Text, nullable=False)
    timestamp = Column(
        DateTime,
        nullable=False,
        index=True,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
