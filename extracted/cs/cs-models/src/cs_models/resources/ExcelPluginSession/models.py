"""Models for Excel Plugin Sessions."""
import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, Enum, Index
from sqlalchemy.orm import relationship

from ...database import Base


class ExcelPluginSessionStatus(str, enum.Enum):
    active = "active"
    closed = "closed"


class ExcelPluginSessionModel(Base):
    """Model for storing Excel Plugin Sessions.

    Tracks user sessions when interacting with the Excel plugin.
    Each session corresponds to a workbook the user is working with.
    """

    __tablename__ = "excel_plugin_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    org_id = Column(String(128), nullable=True, index=True)
    workbook_name = Column(String(500), nullable=True)
    status = Column(
        Enum(ExcelPluginSessionStatus),
        nullable=False,
        default=ExcelPluginSessionStatus.active,
    )
    last_context = Column(Text, nullable=True)  # JSON stored as text
    session_metadata = Column(Text, nullable=True)  # JSON stored as text
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    # ORM relationships
    queries = relationship(
        "ExcelPluginQueryModel",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_excel_plugin_session_user_status", "user_id", "status"),
    )
