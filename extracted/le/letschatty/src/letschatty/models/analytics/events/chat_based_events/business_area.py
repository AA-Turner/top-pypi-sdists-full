from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from pydantic import Field
from typing import ClassVar
from ....utils.types.identifier import StrObjectId
from datetime import datetime
from typing import Optional
import json

class BusinessAreaData(CustomerEventData):
    business_area_id: StrObjectId
    entered_at: Optional[datetime] = None
    exited_at: Optional[datetime] = None

class ChatBusinessAreaEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: BusinessAreaData

    VALID_TYPES: ClassVar[set] = {
        EventType.BUSINESS_AREA_ASSIGNED,
        EventType.BUSINESS_AREA_REMOVED
    }


    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump
