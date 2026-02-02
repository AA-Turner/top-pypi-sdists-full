from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship

from ...database import Base


class WorkbookBlockCommentModel(Base):
    __tablename__ = "workbook_block_comments"

    id = Column(Integer, primary_key=True)
    block_id = Column(
        Integer,
        ForeignKey("workbook_blocks.id"),
        nullable=False,
    )
    user_id = Column(String(128), nullable=False)
    sequence_number = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
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
    workbook_block = relationship(
        "WorkbookBlockModel",
        back_populates="comments",
    )
