"""Models for Excel Plugin Queries."""
import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship

from ...database import Base


class ExcelPluginQueryStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ExcelPluginQueryModel(Base):
    """Model for storing Excel Plugin Queries.

    Tracks each query made through the Excel plugin, including the
    workbook context, generated operations, and execution metadata.
    """

    __tablename__ = "excel_plugin_queries"

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey("excel_plugin_sessions.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    user_id = Column(String(128), nullable=False, index=True)
    query_text = Column(Text, nullable=False)
    workbook_context = Column(Text, nullable=True)  # JSON stored as text
    response = Column(Text, nullable=True)  # JSON stored as text (includes operations)
    operations_count = Column(Integer, nullable=True, default=0)
    processing_time_ms = Column(Integer, nullable=True)
    status = Column(
        Enum(ExcelPluginQueryStatus),
        nullable=False,
        default=ExcelPluginQueryStatus.pending,
    )
    error_message = Column(Text, nullable=True)
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
    session = relationship(
        "ExcelPluginSessionModel",
        back_populates="queries",
    )
    feedback = relationship(
        "ExcelPluginFeedbackModel",
        back_populates="query",
        uselist=False,  # One-to-one relationship
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_excel_plugin_query_user_created", "user_id", "created_at"),
        Index("idx_excel_plugin_query_status", "status"),
    )
