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


class NCTDesignOutcomesModel(Base):
    __tablename__ = "nct_design_outcomes"

    id = Column(Integer, primary_key=True)
    nct_study_id = Column(
        Integer,
        ForeignKey('nct_study.id'),
        nullable=False,
    )
    outcome_type = Column(String(128))
    measure = Column(Text, nullable=True)
    time_frame = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    last_update_submitted_qc_date = Column(DateTime, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
