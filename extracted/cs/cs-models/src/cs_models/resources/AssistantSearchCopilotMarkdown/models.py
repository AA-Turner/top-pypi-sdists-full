from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
)

from ...database import Base


class AssistantSearchCopilotMarkdownModel(Base):
    __tablename__ = "assistant_search_copilot_markdown"

    id = Column(Integer, primary_key=True)
    search_copilot_id = Column(
        Integer,
        ForeignKey("assistant_search_copilot.id"),
        nullable=True,
    )
    artifact_id = Column(String(50), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
