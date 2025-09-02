from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....utils.types.source_types import SourceType
from enum import StrEnum
from pydantic import Field, field_validator, ValidationInfo
from typing import Optional, ClassVar
from ....utils.types.identifier import StrObjectId
from ....utils.definitions import Area
from .....models.chat.chat_status_modifications import ChatStatusModification
import json

class ChatCreatedFrom(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    SYSTEM = "system"

class ChatStatusEventData(CustomerEventData):
    contact_point_id: Optional[StrObjectId] = None
    template_name: Optional[str] = None
    created_from: Optional[ChatCreatedFrom] = None
    action_type: Optional[ChatStatusModification] = None
    destination_agent_id: Optional[StrObjectId] = None
    area: Area

class ChatStatusEvent(Event):
    data: ChatStatusEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.CHAT_CREATED,
        EventType.CHAT_STATUS_UPDATED,
        EventType.CHAT_DELETED
    }

    @field_validator('type')
    def validate_event_type(cls, value):
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid type for NewChatEvent: {value}")
        return value

    @field_validator('data')
    def validate_data_fields(cls, v: ChatStatusEventData, info: ValidationInfo):
        if info.data.get('type') == EventType.CHAT_CREATED and not v.created_from:
            raise ValueError("created_from must be set for CHAT_CREATED events")
        if info.data.get('type') == EventType.CHAT_STATUS_UPDATED and not v.action_type:
            raise ValueError("action_type must be set for CHAT_STATUS_UPDATED events")
        if info.data.get('type') == EventType.CHAT_STATUS_UPDATED and v.action_type == ChatStatusModification.ASSIGN and not v.destination_agent_id:
            raise ValueError("destination_agent_id must be set for CHAT_STATUS_UPDATED events when action_type is ASSIGN")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump