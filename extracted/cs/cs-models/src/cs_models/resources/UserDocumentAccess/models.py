from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class UserDocumentAccessModel(Base):
    __tablename__ = 'user_document_access'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    user_document_id = Column(
        Integer,
        ForeignKey('user_documents.id'),
        nullable=False,
    )
    provider_permission_id = Column(String(255), nullable=True)
    is_inherited = Column(Boolean, default=False)
    source_provider = Column(String(32), nullable=True)
    is_deleted = Column(Boolean, default=False)
    synced_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
