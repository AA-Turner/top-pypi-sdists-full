from typing import Optional, ClassVar
import json
from pydantic import Field

from .chat_based_event import CustomerEventData
from ..base import Event
from ..event_types import EventType


class ChatResetData(CustomerEventData):
    reset_message_id: Optional[str] = Field(
        default=None,
        description="Message id that triggered the reset (if available)"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Optional reason or trigger for the reset"
    )


class ChatResetEvent(Event):
    data: ChatResetData

    VALID_TYPES: ClassVar[set] = {
        EventType.CHAT_RESET
    }

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump["data"] = self.data.model_dump_json()
        return dump
