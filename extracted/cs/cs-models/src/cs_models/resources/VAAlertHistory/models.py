from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
)
from datetime import datetime

from cs_models.database import Base


class VAAlertHistoryModel(Base):
    """
    VA Alert History table.
    Logs every time an alert is triggered and an email is sent.
    """
    __tablename__ = 'va_alert_history'

    id = Column(Integer, primary_key=True)
    user_va_alert_id = Column(
        Integer,
        ForeignKey('user_va_alerts.id'),
        nullable=False,
    )
    user_id = Column(String(255), nullable=False, index=True)
    threshold_percent = Column(Float, nullable=False)
    old_value = Column(Float, nullable=True)
    new_value = Column(Float, nullable=True)
    actual_change_percent = Column(Float, nullable=False)
    old_revision_date = Column(DateTime, nullable=True)
    new_revision_date = Column(DateTime, nullable=True)
    email_sent_at = Column(DateTime, nullable=True)
    email_status = Column(String(50), default='pending', nullable=False, index=True)  # 'pending', 'sent', 'failed'
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
