from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    Boolean
)

from ...database import Base


class LicensingCollabOutboxModel(Base):
    __tablename__ = "licensing_collab_outbox"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    news_id = Column(
        Integer,
        ForeignKey('newswires.id'),
        nullable=False,
    )
    upfronts = Column(Text, nullable=True)
    milestones = Column(Text, nullable=True)
    sentences = Column(Text, nullable=True)
    reviewed = Column(Boolean, nullable=True)
    historical = Column(Boolean, nullable=True)
    llm_output = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
