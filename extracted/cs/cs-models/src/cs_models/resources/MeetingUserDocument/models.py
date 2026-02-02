from datetime import datetime

from sqlalchemy import (
    Column,
    Text,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from ...database import Base


class MeetingUserDocumentModel(Base):
    __tablename__ = "meeting_user_documents"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(
        Integer,
        ForeignKey('meetings.id'),
        nullable=False,
    )
    user_document_id = Column(
        Integer,
        ForeignKey('user_documents.id'),
        nullable=False,
    )
    status = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=True)
    details = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
