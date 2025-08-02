from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    DECIMAL,
    String,
)

from ...database import Base


class MergerAmountModel(Base):
    __tablename__ = "merger_amounts"

    id = Column(Integer, primary_key=True)
    merger_id = Column(
        Integer,
        ForeignKey('mergers.id'),
        nullable=False,
    )
    deal_value = Column(DECIMAL(13, 2), nullable=False)
    currency = Column(String(10), nullable=False)
    type = Column(String(50), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
