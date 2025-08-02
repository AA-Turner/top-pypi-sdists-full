from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
)
from datetime import datetime

from ...database import Base


class UserDocumentChunkModel(Base):
    __tablename__ = 'user_document_chunks'

    id = Column(Integer, primary_key=True)
    user_document_id = Column(
        Integer,
        ForeignKey('user_documents.id'),
        nullable=False,
    )
    chunk_cui = Column(String(50), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_embedding = Column(Text, nullable=False)
    embedding_source = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
