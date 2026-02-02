"""
UserNCTAlertModel - User subscription for clinical trial change alerts.

Users can subscribe to specific NCT studies to receive notifications
when changes are detected by the NCT ETL pipeline.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from ...database import Base


class UserNCTAlertModel(Base):
    """
    User subscription for NCT clinical trial alerts.

    Each record represents a user's subscription to receive notifications
    about changes to a specific clinical trial (NCT study).

    Attributes:
        id: Primary key
        user_id: Auth0 user ID (e.g., "auth0|123456")
        nct_study_id: Foreign key to NCTStudyModel
        is_active: Whether the subscription is active
        is_deleted: Soft delete flag
        last_notified_at: Timestamp of last notification sent
        last_notified_change_id: ID of last NCTChangeModel processed (for incremental notifications)
        created_at: Record creation timestamp
        updated_at: Record update timestamp
    """

    __tablename__ = "user_nct_alert"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False, index=True)
    nct_study_id = Column(
        Integer,
        ForeignKey("nct_study.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Status flags
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Tracking for incremental notifications
    last_notified_at = Column(DateTime, nullable=True)
    last_notified_change_id = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)

    # Relationships
    nct_study = relationship("NCTStudyModel", backref="user_alerts")

    # Composite indexes for common queries
    __table_args__ = (
        Index("idx_user_nct_alert_active", "is_active", "is_deleted"),
        Index("idx_user_nct_alert_user_study", "user_id", "nct_study_id"),
    )
