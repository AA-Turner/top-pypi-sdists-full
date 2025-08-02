from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
)

from ...database import Base


class MergerOutboxCompanyModel(Base):
    __tablename__ = "merger_outbox_companies"

    id = Column(Integer, primary_key=True)
    merger_outbox_id = Column(
        Integer,
        ForeignKey('merger_outbox.id'),
        nullable=False,
    )
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
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
