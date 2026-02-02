from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Float,
    String
)

from ...database import Base


class JournalScoreModel(Base):
    __tablename__ = "journal_scores"

    id = Column(Integer, primary_key=True)
    issn = Column(String(50), nullable=False, index=True)
    sjr_score = Column(Float, nullable=True)
    best_quartile = Column(Integer, nullable=True)
    h_index = Column(Float, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
