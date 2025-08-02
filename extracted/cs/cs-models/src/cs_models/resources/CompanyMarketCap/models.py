from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    DECIMAL,
)
from datetime import datetime

from ...database import Base


class CompanyMarketCapModel(Base):
    __tablename__ = 'company_market_cap'

    id = Column(Integer, primary_key=True)
    company_id = Column(
        String(50),
        nullable=False,
        index=True
    )
    market_cap = Column(DECIMAL(20, 2), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
