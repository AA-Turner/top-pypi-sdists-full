"""
NCTAlertHistoryModel - Audit trail for NCT alert notifications.

Tracks all alert notifications sent to users, including the specific
changes that were included and the delivery status.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
)

from ...database import Base


class NCTAlertHistoryModel(Base):
    """
    Audit trail for NCT clinical trial alert notifications.

    Each record represents a single change notification sent to a user.
    Multiple records with the same batch_id indicate they were sent
    in the same digest email.

    Attributes:
        id: Primary key
        user_nct_alert_id: Foreign key to UserNCTAlertModel subscription
        user_id: Auth0 user ID (denormalized for efficient queries)
        nct_change_id: Foreign key to NCTChangeModel (the actual change)
        nct_study_id: Foreign key to NCTStudyModel (denormalized)
        change_type: Type of change (e.g., "STATUS_CHANGE", "PHASE_CHANGE")
        old_value: Previous value (denormalized for audit)
        new_value: New value (denormalized for audit)
        email_status: Delivery status ("pending", "sent", "failed")
        email_sent_at: Timestamp when email was sent
        email_message_id: SES message ID for tracking
        batch_id: Groups changes sent in same digest email
        created_at: Record creation timestamp
    """

    __tablename__ = "nct_alert_history"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # References
    user_nct_alert_id = Column(
        Integer,
        ForeignKey("user_nct_alert.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(String(255), nullable=False, index=True)
    nct_change_id = Column(
        Integer,
        ForeignKey("nct_changes.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    nct_study_id = Column(
        Integer,
        ForeignKey("nct_study.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    # Denormalized change details for audit/reporting
    change_type = Column(String(50), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    # Email delivery status
    email_status = Column(String(50), default="pending", nullable=False, index=True)
    email_sent_at = Column(DateTime, nullable=True)
    email_message_id = Column(String(255), nullable=True)

    # Batch tracking (groups changes sent in same digest email)
    batch_id = Column(String(100), nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Composite indexes for common queries
    __table_args__ = (
        Index("idx_nct_alert_history_user_status", "user_id", "email_status"),
        Index("idx_nct_alert_history_batch", "batch_id", "email_status"),
    )
