from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    String,
    DECIMAL,
    Boolean,
)

from ...database import Base


class IPOOutboxModel(Base):
    __tablename__ = "ipo_outbox"

    id = Column(Integer, primary_key=True)
    ipo_date = Column(DateTime, nullable=False)
    news_id = Column(
        Integer,
        ForeignKey('newswires.id'),
        nullable=False,
    )
    deal_value = Column(DECIMAL(13, 2), nullable=True)
    currency = Column(String(10), nullable=True)
    price = Column(String(50), nullable=True)
    ticker = Column(String(20), nullable=True)
    type = Column(String(50), nullable=True)
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
    underwriters = Column(Text, nullable=True)
    counsels = Column(Text, nullable=True)
    reviewed = Column(Boolean, nullable=True)
    llm_output = Column(Text, nullable=True)
    historical = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
