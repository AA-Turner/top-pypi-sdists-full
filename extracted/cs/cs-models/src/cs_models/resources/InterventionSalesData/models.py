from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    Text,
)

from ...database import Base


class InterventionSalesDataModel(Base):
    __tablename__ = "intervention_sales_data"

    id = Column(Integer, primary_key=True)
    source_type = Column(
        String(50),
        nullable=False
    )
    date = Column(DateTime, nullable=True)
    news_id = Column(
        Integer,
        ForeignKey('newswires.id'),
        nullable=True,
    )
    company_filing_id = Column(
        Integer,
        ForeignKey('company_filings.id'),
        nullable=True,
    )
    sec_filing_id = Column(
        Integer,
        ForeignKey('companies_sec_filings.id'),
        nullable=True,
    )
    sales_id = Column(
        Integer,
        ForeignKey('sales.id'),
        nullable=True,
    )
    info = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
