from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
)

from ...database import Base


class InterventionInterventionSalesDataModel(Base):
    __tablename__ = "intervention_intervention_sales_data"

    id = Column(Integer, primary_key=True)
    intervention_id = Column(
        Integer,
        ForeignKey('interventions.id'),
        nullable=False,
    )
    intervention_sales_data_id = Column(
        Integer,
        ForeignKey('intervention_sales_data.id'),
        nullable=False,
    )
    score = Column(
        Float,
        nullable=False,
    )
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
