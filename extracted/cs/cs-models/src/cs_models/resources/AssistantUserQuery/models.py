import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ...database import Base
from ..AssistantCommand.models import AssistantCommandModel


class AssistantUserQueryStatusEnum(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"


class AssistantUserQueryModel(Base):
    __tablename__ = "assistant_user_queries"

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey("assistant_sessions.id"),
        nullable=False,
    )
    value = Column(
        String,
        nullable=False,
    )
    filter = Column(
        Text,
        nullable=True,
    )
    type = Column(
        String,
        nullable=False,
    )
    status = Column(
        "status",
        Enum(AssistantUserQueryStatusEnum),
        default=AssistantUserQueryStatusEnum.NOT_STARTED,
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    # These are ORM fields. Don't need to be added in the corresponding migration.
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship
    session = relationship(
        "AssistantSessionModel",
        back_populates="user_queries",
    )
    commands = relationship(
        "AssistantCommandModel",
        order_by=AssistantCommandModel.step_number,
        back_populates="user_query",
    )
