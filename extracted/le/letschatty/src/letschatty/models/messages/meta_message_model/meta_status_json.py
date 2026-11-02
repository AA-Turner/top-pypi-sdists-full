from datetime import datetime
from typing import Optional, Any, Dict

from .meta_base_notification_json import BaseMetaNotificationJson
from .schema.values.value_statuses import StatusNotification, Conversation, Pricing, ErrorDetail
from ...utils.types import Status

class MetaStatusJson(BaseMetaNotificationJson):
    pass

    @property
    def status(self) -> StatusNotification:
        return self.get_value().statuses[0]

    def get_message_wamid(self) -> str:
        return self.status.id

    def get_status_time(self) -> datetime:
        return self.status.timestamp

    def get_errors(self) -> Optional[ErrorDetail]:
        if self.status.errors is not None:
            return self.status.errors[0]
        else:
            return None

    def get_status_value(self) -> Status:
        """The Status enum member for this notification. `played` is a first-class member
        (voice-note receipt); a status Meta adds that we don't manage fails at parse."""
        return self.status.status

    def get_client_wa_id(self) -> Optional[str]:
        # Phase 2: may be None — a status for a message SENT to a BSUID (phone-less chat)
        # carries only recipient_user_id. Callers must fall back to get_client_user_id().
        return self.status.recipient_id

    def get_client_user_id(self) -> Optional[str]:
        """The recipient's BSUID — present when the message was sent to a BSUID; the
        identity fallback when the phone (recipient_id) is absent."""
        return self.status.recipient_user_id

    def get_conversation(self) -> Optional[Conversation]:
        return self.status.conversation

    def get_pricing(self) -> Optional[Pricing]:
        return self.status.pricing
