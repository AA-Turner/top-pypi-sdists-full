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


class UserFileModel(Base):
    __tablename__ = 'user_files'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
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
