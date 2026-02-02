from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, Text, String, UniqueConstraint
from sqlalchemy.orm import relationship

from ...database import Base
from ..WorkbookBlockComment.models import WorkbookBlockCommentModel


class WorkbookBlockModel(Base):
    __tablename__ = "workbook_blocks"

    id = Column(Integer, primary_key=True)
    workbook_id = Column(
        Integer,
        ForeignKey("workbooks.id"),
        nullable=False,
    )
    block_uid = Column(String(64), nullable=False)
    sequence_number = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    data = Column(Text, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    # These are ORM fields. Don't need to be added in the corresponding migration.
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship
    workbook = relationship(
        "WorkbookModel",
        back_populates="blocks",
    )

    comments = relationship(
        "WorkbookBlockCommentModel",
        primaryjoin="and_(WorkbookBlockModel.id==WorkbookBlockCommentModel.block_id, "
                    "or_(WorkbookBlockCommentModel.is_deleted==False, WorkbookBlockCommentModel.is_deleted==None))",
        order_by=WorkbookBlockCommentModel.sequence_number,
        back_populates="workbook_block",
    )

    __table_args__ = (
        UniqueConstraint('workbook_id', 'block_uid', name='uq_workbook_block_uid'),
    )
