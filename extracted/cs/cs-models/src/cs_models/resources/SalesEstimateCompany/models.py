from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class SalesEstimateCompanyModel(Base):
    __tablename__ = 'sales_estimate_companies'

    id = Column(Integer, primary_key=True)
    company_sec_id = Column(
        Integer,
        ForeignKey('companies_sec.id'),
        nullable=True,
    )
    company_ous_id = Column(
        Integer,
        ForeignKey('companies_ous.id'),
        nullable=True,
    )
    sales_estimate_id = Column(
        Integer,
        ForeignKey('sales_estimates.id'),
        nullable=False,
    )
    date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
