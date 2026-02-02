from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    Boolean,
)

from ...database import Base


class CollectionEntityModel(Base):
    __tablename__ = "collection_entities"

    id = Column(Integer, primary_key=True)
    collection_id = Column(
        Integer,
        ForeignKey('collections.id'),
        nullable=False,
    )
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(50), nullable=False)
    entity_name = Column(String(256), nullable=False)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
