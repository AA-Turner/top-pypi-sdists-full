from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    String,
    Boolean,
)

from ...database import Base


class SearchLinkModel(Base):
    __tablename__ = "search_links"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    type = Column(String(50), nullable=False)
    payload = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
