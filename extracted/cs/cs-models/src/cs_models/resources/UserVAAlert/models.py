from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
)
from datetime import datetime

from cs_models.database import Base


class UserVAAlertModel(Base):
    """
    User VA Alert configuration table.
    Stores per-parameter threshold settings for Visible Alpha alerts.
    """
    __tablename__ = 'user_va_alerts'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False, index=True)
    va_parameter_id = Column(
        Integer,
        ForeignKey('va_parameters.id'),
        nullable=False,
    )
    period = Column(String(50), nullable=False)
    threshold_percent = Column(Float, nullable=False)  # e.g., 5.0 for 5%
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    last_checked_at = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
