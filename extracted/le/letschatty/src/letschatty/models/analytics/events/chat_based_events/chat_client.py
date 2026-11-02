from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from typing import ClassVar
import json


class ChatClientEvent(Event):
    """Emitted when the client (contact/customer) data on a chat is updated."""
    data: CustomerEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.CHAT_CLIENT_UPDATED,
    }

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump
