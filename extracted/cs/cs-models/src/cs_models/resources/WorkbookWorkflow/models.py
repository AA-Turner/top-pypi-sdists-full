from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    String,
    ForeignKey,
)
from datetime import datetime
from sqlalchemy.orm import relationship

from ...database import Base
from ..WorkbookWorkflowBlock.models import WorkbookWorkflowBlockModel


class WorkbookWorkflowModel(Base):
    __tablename__ = 'workbook_workflows'

    id = Column(Integer, primary_key=True)
    workbook_id = Column(
        Integer,
        ForeignKey("workbooks.id"),
        nullable=False,
    )
    status = Column(String(50), nullable=False)
    is_completed = Column(Boolean, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    workflow_blocks = relationship(
        "WorkbookWorkflowBlockModel",
        primaryjoin="WorkbookWorkflowModel.id==WorkbookWorkflowBlockModel.workflow_id",
        order_by=WorkbookWorkflowBlockModel.sequence_number,
        back_populates="workbook_workflow",
    )
