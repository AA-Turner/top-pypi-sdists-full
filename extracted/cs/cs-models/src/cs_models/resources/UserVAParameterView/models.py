from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from datetime import datetime

from ...database import Base


class UserVAParameterViewModel(Base):
    __tablename__ = 'user_va_parameter_views'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    condition_norm = Column(String(191), index=True, nullable=False)
    is_deleted = Column(Boolean, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
