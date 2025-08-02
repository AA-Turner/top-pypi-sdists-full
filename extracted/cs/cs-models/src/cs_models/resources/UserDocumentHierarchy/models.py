from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from ...database import Base


class UserDocumentHierarchyModel(Base):
    __tablename__ = 'user_documents_hierarchy'

    id = Column(Integer, primary_key=True)
    provider_id = Column(String(128), nullable=False, index=True)
    user_id = Column(String(128), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    document_name = Column(String(255), nullable=True)
    parent_id = Column(
        Integer,
        ForeignKey('user_documents_hierarchy.id'),
        nullable=True
    )
    is_folder = Column(Boolean, nullable=True)
    user_document_id = Column(
        Integer,
        ForeignKey('user_documents.id'),
        nullable=True,
    )
    workbook_id = Column(
        Integer,
        ForeignKey('workbooks.id'),
        nullable=True,
    )
    sha1 = Column(String(40), nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    is_trashed = Column(Boolean, nullable=True)
    is_locked = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    children = relationship("UserDocumentHierarchyModel", backref='parent', remote_side=[id])
