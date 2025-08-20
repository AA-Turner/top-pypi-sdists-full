from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from datetime import datetime
from ...database import Base


class WorkbookMetaModel(Base):
    __tablename__ = 'workbook_meta'
    workbook_id = Column(Integer, ForeignKey("workbooks.id"), primary_key=True)
    version = Column(Integer, nullable=False, default=0)
