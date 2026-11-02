from typing import Optional
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from enum import StrEnum
from ...messages.chatty_messages import ChattyMessage
from ...base_models import ChattyAssetModel
from ...utils.types.identifier import StrObjectId

class NotificationType(StrEnum):
    NEW_CHAT = "new_chat"
    NEW_MESSAGE = "new_message"
    NEW_ASSIGNMENT = "new_assignment"
    STOLEN_CHAT = "stolen_chat"
    SUGGESTION = "suggestion"
    NEW_SOURCE = "new_source"


class Notification(ChattyAssetModel):
    notification_type: NotificationType
    message : ChattyMessage
    notification_timestamp: datetime
    notification_read: bool = Field(default=False, description="If true, the notification has been read")
    whatsapp_wamid: Optional[str] = Field(default=None, description="The WhatsApp WAMID of the notification in case it was sent via WhatsApp")

class NotificationScope(StrEnum):
    ALL = "all"
    ASSIGNED_OR_RELEVANT = "assigned_or_relevant"
    ASSIGNED = "assigned"

class WhatsAppNotifications(BaseModel):
    active: bool = Field(default=False, description="If true, the notification will be sent to the user via WhatsApp")
    expiration_date: datetime = Field(description="The expiration date of the notification")

    @classmethod
    def default(cls):
        return cls(
            active=False,
            expiration_date=datetime.now(tz=ZoneInfo("UTC")) - timedelta(days=1)
        )

class NotificationSettings(BaseModel):
    enabled: bool = Field(default=True, description="If true, the user will receive notifications")
    whatsapp_notifications: WhatsAppNotifications = Field(default=WhatsAppNotifications.default(), description="The settings for WhatsApp notifications")
    scope: NotificationScope = Field(default=NotificationScope.ASSIGNED_OR_RELEVANT, description="The scope of the notifications")