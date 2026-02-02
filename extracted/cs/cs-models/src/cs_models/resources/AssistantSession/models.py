"""Models for storing Mindgram assistant sessions."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..AssistantUserQuery.models import AssistantUserQueryModel
from ...database import Base


class AssistantSessionModel(Base):
    """Model for storing Assistant Session."""

    __tablename__ = "assistant_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    type = Column(String(50), nullable=False)
    label = Column(String(128), nullable=False)
    display_label = Column(String(128), nullable=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    is_deleted = Column(Boolean, nullable=True)
    internal_doc_only = Column(Boolean, nullable=True)
    workbook_id = Column(
        Integer,
        ForeignKey("workbooks.id"),
        nullable=True,
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
    user_queries = relationship(
        "AssistantUserQueryModel",
        order_by=AssistantUserQueryModel.created_at,
        back_populates="session",
    )
