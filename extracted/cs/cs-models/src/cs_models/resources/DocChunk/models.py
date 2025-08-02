from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
)

from ...database import Base


class DocChunkModel(Base):
    __tablename__ = "doc_chunks"

    id = Column(Integer, primary_key=True)
    artifact_id = Column(String(50), nullable=False)
    chunk_cui = Column(String(50), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_embedding = Column(Text, nullable=False)
    embedding_source = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=True)
    is_indexed = Column(Boolean, nullable=True)
    indexed_date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
