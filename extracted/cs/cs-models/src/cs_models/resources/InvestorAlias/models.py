from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    ForeignKey,
)

from ...database import Base


class InvestorAliasModel(Base):
    __tablename__ = "investor_aliases"

    id = Column(Integer, primary_key=True)
    alias = Column(String(191), nullable=False)
    investor_id = Column(
        Integer,
        ForeignKey('investors.id'),
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
