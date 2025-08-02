from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
)

from ...database import Base


class InvestorBucketModel(Base):
    __tablename__ = "investor_bucket"

    id = Column(Integer, primary_key=True)
    name = Column(String(191), nullable=False, index=True)
    website = Column(String(256), nullable=True)
    type = Column(String(50), nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
