from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Text,
    String,
)

from ...database import Base


class InterventionDataInfoModel(Base):
    __tablename__ = "intervention_data_info"

    id = Column(Integer, primary_key=True)
    table_name = Column(String(50), nullable=False)
    table_id = Column(Integer, nullable=False)
    info = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
