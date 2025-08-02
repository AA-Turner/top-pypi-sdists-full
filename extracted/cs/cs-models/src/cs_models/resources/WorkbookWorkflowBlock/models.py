from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship
from ...database import Base


class WorkbookWorkflowBlockModel(Base):
    __tablename__ = "workbook_workflow_blocks"

    id = Column(Integer, primary_key=True)
    workflow_id = Column(
        Integer,
        ForeignKey("workbook_workflows.id"),
        nullable=False,
    )
    sequence_number = Column(Integer, nullable=False)
    block_type = Column(String(50), nullable=False)
    data = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)
    rendered = Column(Boolean, nullable=True)
    is_completed = Column(Boolean, nullable=True)
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
    workbook_workflow = relationship(
        "WorkbookWorkflowModel",
        back_populates="workflow_blocks",
    )
