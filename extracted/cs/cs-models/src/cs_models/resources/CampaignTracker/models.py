from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
)

from ...database import Base


class CampaignTrackerModel(Base):
    __tablename__ = "campaign_tracker"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=True)
    company = Column(String(128), nullable=True)
    promo_code = Column(String(50), nullable=True)
    campaign_description = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
