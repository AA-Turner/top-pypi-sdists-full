from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    UniqueConstraint,
)
from datetime import datetime

from ...database import Base


class PatentApplicationModel(Base):
    __tablename__ = 'patent_applications'

    id = Column(Integer, primary_key=True)
    application_number = Column(String(128), nullable=False)
    document_number = Column(String(128), nullable=True)
    jurisdiction = Column(String(128), nullable=False)
    app_grp_art_number = Column(Integer, nullable=True)
    abstract_text = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    filed_date = Column(DateTime, nullable=True)
    published_date = Column(DateTime, nullable=True)
    inventors = Column(Text, nullable=True)
    applicant = Column(Text, nullable=True)
    app_class = Column(String(20), nullable=True)
    app_sub_class = Column(String(20), nullable=True)
    title = Column(String(500))
    docdb_family_id = Column(Integer, nullable=True)
    inpadoc_family_id = Column(Integer, nullable=True)
    is_orange_book = Column(Boolean, nullable=True)
    is_purple_book = Column(Boolean, nullable=True)

    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    __table_args__ = (UniqueConstraint('application_number', 'jurisdiction'),)
