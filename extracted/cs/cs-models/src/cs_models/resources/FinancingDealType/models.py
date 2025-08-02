from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)

from ...database import Base


class FinancingDealTypeModel(Base):
    __tablename__ = "financing_deal_types"

    id = Column(Integer, primary_key=True)
    deal_type = Column(
        String(128),
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
