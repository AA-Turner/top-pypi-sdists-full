from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
)

from ...database import Base


class IPOUnderwriterModel(Base):
    __tablename__ = "ipo_underwriters"

    id = Column(Integer, primary_key=True)
    ipo_id = Column(
        Integer,
        ForeignKey('ipos.id'),
        nullable=False,
    )
    underwriter_id = Column(
        Integer,
        ForeignKey('investors.id'),
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
