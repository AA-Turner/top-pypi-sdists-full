from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from ...database import Base


class PatentIFWModel(Base):
    __tablename__ = 'patent_ifws'

    id = Column(Integer, primary_key=True)
    patent_id = Column(
        Integer,
        ForeignKey('patents.id'),
        nullable=True,
    )
    patent_application_id = Column(
        Integer,
        ForeignKey('patent_applications.id'),
        nullable=False,
    )
    appl_id = Column(String(128), nullable=False)
    document_identifier = Column(String(50), nullable=False)
    document_code = Column(String(50), nullable=True)
    document_description = Column(String(256), nullable=True)
    direction_category = Column(String(50), nullable=True)
    official_date = Column(DateTime, nullable=True)
    total_pages = Column(Integer, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
