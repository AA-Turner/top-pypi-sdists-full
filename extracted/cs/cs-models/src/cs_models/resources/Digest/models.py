from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
)

from ...database import Base


class DigestModel(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True)
    saved_search_id = Column(
        Integer,
        ForeignKey('user_saved_searches.id'),
        nullable=False,
    )
    user_id = Column(String(128), nullable=True, index=True)
    type = Column(String(128), nullable=False)
    description = Column(String(256), nullable=False)
    created_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
