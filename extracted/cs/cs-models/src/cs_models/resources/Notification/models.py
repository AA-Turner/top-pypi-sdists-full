from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Float,
)
from datetime import datetime

from ...database import Base


class NotificationModel(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    saved_search_id = Column(
        Integer,
        ForeignKey('user_saved_searches.id'),
        nullable=False,
    )
    source_type = Column(String(50), nullable=False)
    source_table = Column(String(50), nullable=False)
    artifact_id = Column(String(128), nullable=False)
    text = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    source_id = Column(Integer, nullable=False)
    source_detail = Column(Text, nullable=False)
    seen_at = Column(DateTime, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    daily_processed_at = Column(DateTime, nullable=True)
    weekly_processed_at = Column(DateTime, nullable=True)
    date = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
