from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
)

from ...database import Base


class MergerOutboxModel(Base):
    __tablename__ = "merger_outbox"

    id = Column(Integer, primary_key=True)
    announcement_date = Column(DateTime, nullable=False)
    news_id = Column(Integer, ForeignKey('newswires.id'), nullable=False)
    deal_value = Column(Text, nullable=True)
    price = Column(Text, nullable=True)
    advisors = Column(Text, nullable=True)
    counsels = Column(Text, nullable=True)
    sentences = Column(Text, nullable=True)
    reviewed = Column(Boolean, nullable=True)
    llm_output = Column(Text, nullable=True)
    historical = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
