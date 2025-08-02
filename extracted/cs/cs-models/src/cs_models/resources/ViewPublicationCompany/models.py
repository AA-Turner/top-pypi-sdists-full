from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
)

from ...database import Base


class ViewPublicationCompanyModel(Base):
    __tablename__ = "_view_publication_companies"

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
    date = Column(DateTime, nullable=False)
    table_name = Column(String(50), nullable=False)
    table_id = Column(Integer, nullable=False)
    source = Column(String(50), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
