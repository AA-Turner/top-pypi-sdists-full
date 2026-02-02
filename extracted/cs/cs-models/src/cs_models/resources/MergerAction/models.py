from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
)

from ...database import Base


class MergerActionModel(Base):
    __tablename__ = "merger_actions"

    id = Column(Integer, primary_key=True)
    acquirer_company = Column(Text, nullable=False)
    target_company = Column(Text, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
