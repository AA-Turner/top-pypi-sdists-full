from datetime import datetime

from sqlalchemy import (
    Column,
    Text,
    Integer,
    DateTime,
    ForeignKey,
)

from ...database import Base


class PubmedMeetingUserDocumentModel(Base):
    __tablename__ = "pubmed_meeting_user_documents"

    id = Column(Integer, primary_key=True)
    pubmed_id = Column(
        Integer,
        ForeignKey('pubmed.id'),
        nullable=False,
    )
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
    details = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
