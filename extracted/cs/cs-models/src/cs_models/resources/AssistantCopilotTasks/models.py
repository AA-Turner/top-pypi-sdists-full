from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    ForeignKey,
)

from ...database import Base


class AssistantCopilotTaskModel(Base):
    __tablename__ = "assistant_copilot_tasks"

    id = Column(Integer, primary_key=True)
    assistant_copilot_id = Column(
        Integer,
        ForeignKey('assistant_copilot.id'),
        nullable=False,
    )
    assistant_search_copilot_id = Column(
        Integer,
        ForeignKey('assistant_search_copilot.id'),
        nullable=True,
    )
    assistant_session_id = Column(
        Integer,
        ForeignKey('assistant_sessions.id'),
        nullable=True,
    )
    task_info = Column(
        Text,
        nullable=True
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
