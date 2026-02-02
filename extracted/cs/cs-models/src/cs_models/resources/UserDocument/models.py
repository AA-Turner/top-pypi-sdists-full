from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
    Text,
)
from datetime import datetime

from ...database import Base


class UserDocumentModel(Base):
    __tablename__ = 'user_documents'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=False,
    )
    date = Column(DateTime, nullable=True)
    title = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    type_score = Column(Float, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    upload_date = Column(DateTime, nullable=False)
    category = Column(String(128), nullable=True)
    metadata_info = Column(Text, nullable=True)
    status = Column(String(128), nullable=True)
    page_count = Column(Integer, nullable=True)
    sell_side_source_id = Column(
        Integer,
        ForeignKey("sell_side_sources.id"),
        nullable=True,
        index=True,
    )
    sell_side_note_type = Column(String(64), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
