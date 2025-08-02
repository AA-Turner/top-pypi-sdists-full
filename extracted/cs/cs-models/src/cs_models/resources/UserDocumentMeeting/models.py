from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from ...database import Base


class UserDocumentMeetingModel(Base):
    __tablename__ = "user_document_meetings"

    id = Column(Integer, primary_key=True)
    user_document_id = Column(
        Integer,
        ForeignKey('user_documents.id'),
        nullable=False,
    )
    meeting_id = Column(
        Integer,
        ForeignKey('meetings.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
