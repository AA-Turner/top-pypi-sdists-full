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


class UserExplorerColumnModel(Base):
    __tablename__ = "user_explorer_columns"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    artifact_ids = Column(Text, nullable=False)
    prompt = Column(String(128), nullable=False)
    result = Column(Text, nullable=True)
    is_completed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
