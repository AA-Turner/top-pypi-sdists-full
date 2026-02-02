from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    DECIMAL,
    Float,
)

from ...database import Base


class SalesEstimateModel(Base):
    __tablename__ = "sales_estimates"

    id = Column(Integer, primary_key=True)
    fiscal_year = Column(Integer, nullable=True)
    request_id = Column(String(20), nullable=True)
    metric = Column(String(50), nullable=True)
    drug_name = Column(String(128), nullable=False, index=True)
    company_name = Column(String(128), nullable=True, index=True)
    currency = Column(String(20), nullable=True)
    fiscal_end_date = Column(DateTime, nullable=True)
    estimate_date = Column(DateTime, nullable=True)
    estimate_count = Column(Integer, nullable=True)
    mean = Column(DECIMAL(13, 2), nullable=True)
    median = Column(DECIMAL(13, 2), nullable=True)
    sd = Column(Float, nullable=True)
    high = Column(DECIMAL(13, 2), nullable=True)
    low = Column(DECIMAL(13, 2), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
