from sqlalchemy import (
    Integer,
    Column,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
)
from datetime import datetime
from ...database import Base


class NCTRefModel(Base):
    __tablename__ = "nct_refs"

    id = Column(Integer, primary_key=True)
    nct_study_id = Column(
        Integer,
        ForeignKey('nct_study.id'),
        nullable=False,
    )
    pmid = Column(Integer)
    pubmed_id = Column(
        Integer,
        ForeignKey('pubmed.id'),
        nullable=True,
    )
    reference_type = Column(String(50), nullable=True)
    citation = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
