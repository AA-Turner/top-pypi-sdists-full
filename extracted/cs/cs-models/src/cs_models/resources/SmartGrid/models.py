from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship

from ...database import Base
from ..SmartGridCell.models import SmartGridCellModel


class SmartGridModel(Base):
    __tablename__ = "smart_grids"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    workbook_id = Column(
        Integer,
        ForeignKey('workbooks.id'),
        nullable=True,
    )
    table_info = Column(Text, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    cells = relationship(
        "SmartGridCellModel",
        order_by=SmartGridCellModel.row,
        back_populates="smart_grid",
    )
