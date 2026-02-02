from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from ...database import Base


class TranscriptEquityCompanyModel(Base):
    __tablename__ = 'transcripts_equity_companies'

    id = Column(Integer, primary_key=True)
    equity_id = Column(Integer, nullable=False, index=True)
    equity_details = Column(Text, nullable=True)
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
