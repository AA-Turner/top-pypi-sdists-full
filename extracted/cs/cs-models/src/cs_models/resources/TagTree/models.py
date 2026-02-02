from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
)
from datetime import datetime

from ...database import Base


class TagTreeModel(Base):
    __tablename__ = 'tag_tree'

    id = Column(Integer, primary_key=True)
    tag_id = Column(
        Integer,
        ForeignKey('news_tags.id'),
        nullable=False,
    )
    label_name = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    method = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
