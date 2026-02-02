from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class SellSideSourceModel(Base):
    __tablename__ = "sell_side_sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)  # "Morgan Stanley"
    code = Column(String(64), nullable=False, unique=True)    # "MS", "JPM"

    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
        nullable=False,
    )
