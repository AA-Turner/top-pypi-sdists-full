from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    String,
)

from ...database import Base


class AssistantCopilotModel(Base):
    __tablename__ = "assistant_copilot"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    query = Column(String(256), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    llm_result = Column(Text, nullable=True)
    status_code = Column(String(20), nullable=True)
    status = Column(String(191), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
