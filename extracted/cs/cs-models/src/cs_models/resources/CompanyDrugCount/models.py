from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class CompanyDrugCountModel(Base):
    __tablename__ = 'company_drug_count'

    id = Column(Integer, primary_key=True)
    company_id = Column(
        String(50),
        nullable=False,
        index=True
    )
    drug_count = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
