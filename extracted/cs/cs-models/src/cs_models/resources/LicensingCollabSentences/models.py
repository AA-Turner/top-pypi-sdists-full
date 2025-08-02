from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    String,
    Boolean,
)

from ...database import Base


class LicensingCollabSentenceModel(Base):
    __tablename__ = "licensing_collab_sentences"

    id = Column(Integer, primary_key=True)
    licensing_collab_id = Column(
        Integer,
        ForeignKey('licensing_collab.id'),
        nullable=False,
    )
    text = Column(Text, nullable=False, index=True)
    type = Column(String(50), nullable=True)
    llm_output = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
