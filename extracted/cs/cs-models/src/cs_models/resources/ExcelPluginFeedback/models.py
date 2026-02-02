"""Models for Excel Plugin Feedback."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from ...database import Base


class ExcelPluginFeedbackModel(Base):
    """Model for storing Excel Plugin Operation Feedback.

    Tracks the results of operation execution in the Excel plugin,
    including success/failure status and optional user feedback.
    """

    __tablename__ = "excel_plugin_feedback"

    id = Column(Integer, primary_key=True)
    query_id = Column(
        Integer,
        ForeignKey("excel_plugin_queries.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(String(128), nullable=False, index=True)
    operation_results = Column(Text, nullable=False)  # JSON stored as text
    operations_succeeded = Column(Integer, nullable=True)
    operations_total = Column(Integer, nullable=True)
    user_rating = Column(Integer, nullable=True)  # 1-5 scale
    user_comment = Column(Text, nullable=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )

    # ORM relationships
    query = relationship(
        "ExcelPluginQueryModel",
        back_populates="feedback",
    )

    __table_args__ = (
        Index("idx_excel_plugin_feedback_user", "user_id"),
    )
