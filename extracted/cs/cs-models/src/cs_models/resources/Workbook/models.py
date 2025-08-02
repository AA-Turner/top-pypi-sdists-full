from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from datetime import datetime
from sqlalchemy.orm import relationship

from ...database import Base
from ..WorkbookBlock.models import WorkbookBlockModel


class WorkbookModel(Base):
    __tablename__ = 'workbooks'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    workbook_name = Column(String(128), nullable=False)
    is_deleted = Column(Boolean, nullable=True)
    is_public = Column(Boolean, nullable=True)
    is_help_center = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    blocks = relationship(
        "WorkbookBlockModel",
        primaryjoin="and_(WorkbookModel.id==WorkbookBlockModel.workbook_id, "
                    "or_(WorkbookBlockModel.is_deleted==False, WorkbookBlockModel.is_deleted==None))",
        order_by=WorkbookBlockModel.sequence_number,
        back_populates="workbook",
    )
