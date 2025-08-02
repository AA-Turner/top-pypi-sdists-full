from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
)

from ...database import Base


class B3CRSSModel(Base):
    __tablename__ = "b3c_rss"

    id = Column(Integer, primary_key=True)
    article_id = Column(String(128), nullable=False, index=True)
    article_date = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
