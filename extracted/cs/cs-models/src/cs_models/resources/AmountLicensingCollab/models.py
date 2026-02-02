from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    DECIMAL,
    String,
)

from ...database import Base


class AmountLicensingCollabModel(Base):
    __tablename__ = "amount_licensing_collab"

    id = Column(Integer, primary_key=True)
    licensing_collab_id = Column(
        Integer,
        ForeignKey('licensing_collab.id'),
        nullable=False,
    )
    deal_value = Column(DECIMAL(13, 2), nullable=False)
    currency = Column(String(10), nullable=False)
    type = Column(String(50), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
