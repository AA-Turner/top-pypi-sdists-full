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


class UserSavedSearchDigestModel(Base):
    __tablename__ = 'user_saved_search_digests'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    saved_search_id = Column(
        Integer,
        ForeignKey('user_saved_searches.id'),
        nullable=False,
    )
    assistant_user_query_id = Column(
        Integer,
        ForeignKey('assistant_user_queries.id'),
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
