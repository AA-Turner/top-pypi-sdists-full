from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship

from ...database import Base


class WorkbookThreadCommentModel(Base):
    """
    Represents an individual comment within a thread.
    """
    __tablename__ = "workbook_thread_comments"

    id = Column(Integer, primary_key=True)
    thread_id = Column(
        Integer,
        ForeignKey("workbook_comment_threads.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(String(128), nullable=False)
    sequence_number = Column(Integer, nullable=False)  # 1 = initial comment
    comment = Column(Text, nullable=False)

    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    # Relationships
    thread = relationship("WorkbookCommentThreadModel", back_populates="comments")
