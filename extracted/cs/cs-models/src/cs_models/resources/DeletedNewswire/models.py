from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
)
from datetime import datetime

from ...database import Base


class DeletedNewswireModel(Base):
    __tablename__ = 'deleted_newswires'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    source = Column(String(128))
    headline = Column(Text)
    s3_key_name = Column(String(255), nullable=False)
    source_link = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
