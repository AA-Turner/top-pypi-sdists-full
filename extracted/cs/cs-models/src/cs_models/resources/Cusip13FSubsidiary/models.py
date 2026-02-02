from datetime import datetime
from sqlalchemy import String
from ...database import Base
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)


class Cusip13FSubsidiaryModel(Base):
    __tablename__ = 'cusip13f_subsidiaries'

    id = Column(Integer, primary_key=True)
    cusip = Column(String(9), nullable=False)
    subsidiary_id = Column(
        Integer,
        ForeignKey('subsidiaries.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
