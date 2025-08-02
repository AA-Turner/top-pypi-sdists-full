from sqlalchemy import (
    Integer,
    Column,
    String,
    DateTime,
    Text,
    Boolean,
)
from datetime import datetime
from ...database import Base


class NCTStudyModel(Base):
    __tablename__ = "nct_study"

    id = Column(Integer, primary_key=True)
    nct_id = Column(String(128), nullable=False, unique=True)
    acronym = Column(String(128), nullable=True)
    brief_title = Column(Text)
    official_title = Column(Text)
    brief_summary = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    enrollment = Column(Integer, nullable=True)
    enrollment_type = Column(String(50), nullable=True)
    why_stopped = Column(Text, nullable=True)
    primary_completion_date = Column(DateTime, nullable=True)
    primary_completion_date_type = Column(String(128), nullable=True)
    study_completion_date = Column(DateTime, nullable=True)
    study_completion_date_type = Column(String(128), nullable=True)
    study_first_posted_date = Column(DateTime, nullable=True)
    study_status = Column(String(128))
    study_type = Column(String(50))
    study_start_date = Column(DateTime)
    last_update_submitted_qc_date = Column(DateTime)
    phase = Column(Text)
    sponsors = Column(Text, nullable=True)
    conditions = Column(Text, nullable=True)
    interventions = Column(Text, nullable=True)
    industry_flag = Column(Boolean)
    study_keywords = Column(Text)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
