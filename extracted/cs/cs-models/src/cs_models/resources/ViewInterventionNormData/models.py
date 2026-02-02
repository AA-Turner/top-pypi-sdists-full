from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Boolean,
    ForeignKey,
)

from ...database import Base


class ViewInterventionNormDataModel(Base):
    __tablename__ = "_view_intervention_norm_data"

    id = Column(Integer, primary_key=True)
    norm_cui = Column(String(128), nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    table_name = Column(String(50), nullable=False)
    table_id = Column(Integer, nullable=False)
    pivotal = Column(Boolean, nullable=True)
    intervention_data_info_id = Column(
        Integer,
        ForeignKey('intervention_data_info.id'),
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
