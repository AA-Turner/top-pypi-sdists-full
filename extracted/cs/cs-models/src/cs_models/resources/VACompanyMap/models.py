from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class VACompanyMapModel(Base):
    __tablename__ = 'va_company_map'

    id = Column(Integer, primary_key=True)
    cid = Column(Integer, nullable=False, index=True)
    capiqcid = Column(Integer, nullable=True)
    cik = Column(String(191), nullable=False, index=True)
    ticker = Column(String(50), nullable=True)
    name = Column(String(191), nullable=True)
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
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
