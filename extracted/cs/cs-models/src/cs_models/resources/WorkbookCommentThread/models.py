from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship

from ...database import Base
from ..WorkbookThreadComment.models import WorkbookThreadCommentModel


class WorkbookCommentThreadModel(Base):
    """
    Represents a comment thread tied to a text selection in a workbook block.
    """
    __tablename__ = "workbook_comment_threads"

    id = Column(Integer, primary_key=True)
    workbook_id = Column(
        Integer,
        ForeignKey("workbooks.id", ondelete="CASCADE"),
        nullable=False,
    )
    block_uid = Column(String(64), nullable=False)  # Root parent block UID

    # Selection context
    selected_text = Column(Text, nullable=False)  # The highlighted text

    # Thread status
    is_resolved = Column(Boolean, default=False, nullable=False)
    resolved_by = Column(String(128), nullable=True)  # user_id who resolved
    resolved_at = Column(DateTime, nullable=True)

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
    created_by = Column(String(128), nullable=False)  # user_id who created thread

    # Smart Grid Cells
    cell_session_id = Column(Integer, nullable=True)
    cell_user_query_id = Column(Integer, nullable=True)
    text_start_offset = Column(Integer, nullable=True)
    text_end_offset = Column(Integer, nullable=True)

    # Relationships
    workbook = relationship("WorkbookModel", back_populates="comment_threads")

    comments = relationship(
        "WorkbookThreadCommentModel",
        primaryjoin="and_(WorkbookCommentThreadModel.id==WorkbookThreadCommentModel.thread_id, "
                    "or_(WorkbookThreadCommentModel.is_deleted==False, WorkbookThreadCommentModel.is_deleted==None))",
        order_by=WorkbookThreadCommentModel.sequence_number,
        back_populates="thread",
        lazy="joined",  # Eager load comments when loading thread
    )
