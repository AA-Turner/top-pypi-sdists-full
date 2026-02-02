from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
)

from ...database import Base


class CompanyLicensingCollabModel(Base):
    __tablename__ = "company_licensing_collab"

    id = Column(Integer, primary_key=True)
    licensing_collab_id = Column(
        Integer,
        ForeignKey('licensing_collab.id'),
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
    target_flag = Column(
        Boolean,
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
