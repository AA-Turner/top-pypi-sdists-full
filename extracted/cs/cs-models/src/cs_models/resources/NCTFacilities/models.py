from sqlalchemy import (
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey
)
from datetime import datetime
from ...database import Base


class NCTFacilityModel(Base):
    __tablename__ = "nct_facilities"

    id = Column(Integer, primary_key=True)
    nct_study_id = Column(
        Integer,
        ForeignKey('nct_study.id'),
        nullable=False,
    )
    facility_name = Column(String(256))
    facility_city = Column(String(50))
    facility_state = Column(String(50))
    facility_country = Column(String(50))
    facility_zip_code = Column(String(20))
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
