from sqlalchemy import (
    Integer,
    Column,
    String,
    DateTime,
    Text,
    ForeignKey,
)
from datetime import datetime
from ...database import Base


class NCTChangeModel(Base):
    __tablename__ = "nct_changes"

    id = Column(Integer, primary_key=True)
    nct_id = Column(String(50), nullable=False)
    nct_study_id = Column(
        Integer,
        ForeignKey('nct_study.id'),
        nullable=True,
        index=True,
    )
    date = Column(DateTime, nullable=False, index=True)
    change_type = Column(String(50), nullable=False, index=True)
    news_id = Column(
        Integer,
        ForeignKey('newswires.id'),
        nullable=True,
    )
    pubmed_id = Column(
        Integer,
        ForeignKey('pubmed.id'),
        nullable=True,
    )
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    note = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
