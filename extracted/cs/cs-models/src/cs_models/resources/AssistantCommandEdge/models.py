"""Model to capture dependencies among Assistant commands."""
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from ...database import Base
from ..AssistantCommand.models import AssistantCommandModel


class AssistantCommandEdgeModel(Base):
    """Model to capture assistant command dependencies."""

    __tablename__ = "assistant_command_edges"

    lower_id = Column(Integer, ForeignKey("assistant_commands.id"), primary_key=True)
    higher_id = Column(Integer, ForeignKey("assistant_commands.id"), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    lower_node = relationship(
        AssistantCommandModel,
        primaryjoin=lower_id == AssistantCommandModel.id,
        backref="lower_edges",
    )
    higher_node = relationship(
        AssistantCommandModel,
        primaryjoin=higher_id == AssistantCommandModel.id,
        backref="higher_edges",
    )

    def __init__(self, n1, n2):
        self.lower_node = n1
        self.higher_node = n2
