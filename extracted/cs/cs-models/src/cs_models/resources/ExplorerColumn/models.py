from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    Boolean,
    String,
)

from ...database import Base


class ExplorerColumnModel(Base):
    __tablename__ = "explorer_columns"

    id = Column(Integer, primary_key=True)
    artifact_id = Column(
        String(50),
        nullable=False,
        index=True
    )
    prompt = Column(String(128), nullable=False, index=True)
    answer = Column(Text, nullable=True)
    is_completed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
