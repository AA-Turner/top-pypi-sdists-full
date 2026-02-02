from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)

from ...database import Base


class PurpleBookPatentModel(Base):
    __tablename__ = "purple_book_patents"

    id = Column(Integer, primary_key=True)
    bla_number = Column(String(128), nullable=False, index=True)
    applicant_name = Column(String(191), nullable=False, index=True)
    proprietary_name = Column(String(191), nullable=False, index=True)
    proper_name = Column(String(191), nullable=False, index=True)
    patent_number = Column(String(128), nullable=False, index=True)
    expiration_date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        index=True,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
