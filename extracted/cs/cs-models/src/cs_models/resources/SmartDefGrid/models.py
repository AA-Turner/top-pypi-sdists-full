from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from ...database import Base


class SmartDefGridModel(Base):
    """
    One extracted BlockNote table artifact.
    You can link to your workbook/doc via source_* fields.
    """
    __tablename__ = "smart_def_grids"

    id = Column(Integer, primary_key=True, autoincrement=True)  # table_id (uuid string)
    workbook_id = Column(
        Integer,
        ForeignKey('workbooks.id'),
        nullable=True,
        primary_key=True,
    )
    source_block_id = Column(String(64), nullable=True)     # BlockNote block id (if any)

    outline_version = Column(Integer, nullable=False, default=1)   # your normalize() version
    outline_json = Column(JSON, nullable=False)                     # semantic outline payload
    original_table_json = Column(JSON, nullable=False)              # raw BlockNote table node (for rebuilds)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    cells = relationship("SmartDefGridCellModel", back_populates="table", cascade="all, delete-orphan")
