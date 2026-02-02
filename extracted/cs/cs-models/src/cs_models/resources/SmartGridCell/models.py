from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship

from ...database import Base


class SmartGridCellModel(Base):
    __tablename__ = "smart_grid_cells"

    id = Column(Integer, primary_key=True)
    smart_grid_id = Column(
        Integer,
        ForeignKey("smart_grids.id"),
        nullable=False,
    )
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    data = Column(Text, nullable=True)
    user_query_id = Column(
        Integer,
        ForeignKey("assistant_user_queries.id"),
        nullable=True,
    )
    reformulated_question = Column(String(Text), nullable=False)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    user_query = relationship(
        "AssistantUserQueryModel",
    )

    smart_grid = relationship(
        "SmartGridModel",
        back_populates="cells",
    )
