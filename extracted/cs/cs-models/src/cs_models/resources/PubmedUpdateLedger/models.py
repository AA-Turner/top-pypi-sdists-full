from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String
)

from ...database import Base


class PubmedUpdateLedgerModel(Base):
    __tablename__ = "pubmed_update_ledger"

    id = Column(Integer, primary_key=True)
    pubmed_cui = Column(Integer, nullable=False, unique=True)
    file_name_id = Column(Integer, nullable=False)
    file_name = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
