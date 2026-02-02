from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)

from ...database import Base


class ViewPublicationConditionNormModel(Base):
    __tablename__ = "_view_publication_condition_norm"

    id = Column(Integer, primary_key=True)
    condition_norm_cui = Column(String(128), nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    table_name = Column(String(50), nullable=False)
    table_id = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
