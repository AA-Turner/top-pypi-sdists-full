from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Boolean,
)

from ...database import Base


class CollectionModel(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    type = Column(String(50), nullable=False)
    global_access = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
