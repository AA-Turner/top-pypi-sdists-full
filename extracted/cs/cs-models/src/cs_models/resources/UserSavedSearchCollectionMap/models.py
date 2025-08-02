from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class UserSavedSearchCollectionMapModel(Base):
    __tablename__ = 'user_saved_searches_collection_map'

    id = Column(Integer, primary_key=True)
    saved_search_id = Column(
        Integer,
        ForeignKey('user_saved_searches.id'),
        nullable=False,
    )
    collection_id = Column(
        Integer,
        ForeignKey('collections.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
