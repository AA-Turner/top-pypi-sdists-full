from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)

from ...database import Base


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    note_hash = Column(String(64), nullable=False)
    note_heading = Column(String(128), nullable=False)
    note = Column(Text, nullable=False)
    note_insights = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
