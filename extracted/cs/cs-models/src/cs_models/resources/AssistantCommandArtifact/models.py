from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Float,
    String,
    Text,
)

from ...database import Base


class AssistantCommandArtifactModel(Base):
    __tablename__ = "assistant_command_artifacts"

    id = Column(Integer, primary_key=True)
    assistant_command_id = Column(
        Integer,
        ForeignKey('assistant_commands.id'),
        nullable=False,
    )
    artifact_id = Column(String(64), nullable=False)
    score = Column(Float, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
