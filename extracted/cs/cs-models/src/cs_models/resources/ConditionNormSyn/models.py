from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)

from ...database import Base


class ConditionNormSynModel(Base):
    __tablename__ = "condition_norm_syns"

    id = Column(Integer, primary_key=True)
    alias = Column(String(191), nullable=False, index=True)
    condition_norm_cui = Column(String(128), nullable=False, index=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
