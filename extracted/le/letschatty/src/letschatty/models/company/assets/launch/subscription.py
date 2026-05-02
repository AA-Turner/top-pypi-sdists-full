from pydantic import BaseModel, Field
from typing import List, Optional
from letschatty.models.utils.types.identifier import StrObjectId
from datetime import datetime
from enum import StrEnum


class LaunchSubscriptionStatus(StrEnum):
    """
    Status of a user's subscription to a launch.
    Note: Pre-qualification is tracked separately in ChattyAIAgentInChat.pre_qualify_status
    """
    SUBSCRIBED = "subscribed"          # Successfully subscribed
    UNSUBSCRIBED = "unsubscribed"      # User unsubscribed
    ATTENDED = "attended"              # User attended the launch
    MISSED = "missed"                  # User missed the launch


class LaunchSubscription(BaseModel):
    """
    Tracks a chat's subscription to a launch.
    Embedded within the Launch model.
    """
    chat_id: StrObjectId = Field(description="ID of the subscribed chat")
    launch_id: StrObjectId = Field(description="ID of the associated launch")
    status: LaunchSubscriptionStatus = Field(
        default=LaunchSubscriptionStatus.SUBSCRIBED,
        description="Current status of the subscription"
    )
    subscribed_at: datetime = Field(description="Timestamp when the user subscribed")

    # Tracking (optional)
    personal_access_link: Optional[str] = Field(
        default=None,
        description="Unique link for tracking user access to the launch (if tracking enabled)"
    )

    # Communications tracking
    communications_sent: List[str] = Field(
        default_factory=list,
        description="List of IDs of communications already sent to this specific subscriber"
    )

    # Welcome kit tracking
    welcome_kit_sent: bool = Field(
        default=False,
        description="True if the welcome kit has been sent to this subscriber"
    )
    welcome_kit_sent_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the welcome kit was sent"
    )

    # Status timestamps
    attended_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the user attended the launch"
    )
    unsubscribed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the user unsubscribed"
    )

