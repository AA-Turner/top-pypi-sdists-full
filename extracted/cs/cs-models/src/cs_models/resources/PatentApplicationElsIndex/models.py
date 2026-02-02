from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
)

from ...database import Base


class PatentApplicationElsIndexModel(Base):
    __tablename__ = "patent_applications_els_index"

    id = Column(Integer, primary_key=True)
    patent_application_id = Column(
        Integer,
        ForeignKey('patent_applications.id'),
        nullable=False,
    )
    els_indexed = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
