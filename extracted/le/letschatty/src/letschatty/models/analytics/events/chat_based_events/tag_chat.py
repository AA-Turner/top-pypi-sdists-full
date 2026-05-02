from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from typing import ClassVar, Optional
from ....utils.types.identifier import StrObjectId
from ....company.assets.tag import Tag
from pydantic import field_validator, ValidationInfo
from ....utils.types.serializer_type import SerializerType
import json

class TagChatData(CustomerEventData):
    tag_id: StrObjectId
    tag: Tag
    time_to_tag_seconds: Optional[int] = None

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['tag'] = self.tag.model_dump_json(serializer=SerializerType.API) if self.tag else None
        return dump

class TagChatEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: TagChatData

    VALID_TYPES: ClassVar[set] = {
        EventType.TAG_ASSIGNED,
        EventType.TAG_REMOVED
    }


    @field_validator('data')
    def validate_data_fields(cls, v: TagChatData, info: ValidationInfo):
        if info.data.get('type') != EventType.TAG_REMOVED and not v.tag:
            raise ValueError("tag must be set for all events except TAG_REMOVED")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump