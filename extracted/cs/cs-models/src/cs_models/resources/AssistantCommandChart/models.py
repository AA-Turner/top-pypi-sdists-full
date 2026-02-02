from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
)

from ...database import Base


class AssistantCommandChartModel(Base):
    __tablename__ = "assistant_command_charts"

    id = Column(Integer, primary_key=True)
    assistant_command_id = Column(
        Integer,
        ForeignKey('assistant_commands.id'),
        nullable=False,
    )
    file_id = Column(
        Integer,
        ForeignKey('files.id'),
        nullable=False,
    )
    chart_info = Column(Text, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
