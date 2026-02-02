from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from datetime import datetime

from ...database import Base


class UserAutomatedDigestModel(Base):
    __tablename__ = 'user_automated_digests'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    type = Column(String(50), nullable=False)
    type_id = Column(String(50), nullable=False)
    digest_name = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False)
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
