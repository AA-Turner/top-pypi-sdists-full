import json
from typing import ClassVar

from pydantic import model_validator

from ....utils.types.identifier import StrObjectId
from ....push_notifications.enums import NotificationIntentType
from ..base import Event, EventData, EventType
from .metadata import NotificationIntentMetadata


class UserNotificationIntentEventData(EventData):
    chat_id: StrObjectId
    company_id: StrObjectId
    recipient_user_id: StrObjectId
    metadata: NotificationIntentMetadata

    @property
    def message_group_id(self) -> str:
        return f"user-{self.recipient_user_id}"


class UserNotificationIntentEvent(Event):
    data: UserNotificationIntentEventData
    VALID_TYPES: ClassVar[set] = {EventType.USER_NOTIFICATION_INTENT}

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump["data"] = self.data.model_dump_json()
        return dump
