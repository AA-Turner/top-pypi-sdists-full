from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....chat.highlight import Highlight
from ....utils.types.identifier import StrObjectId
from pydantic import Field, field_validator, ValidationInfo
from typing import Optional, ClassVar
from ....utils.types.serializer_type import SerializerType
import json

class HighlightData(CustomerEventData):
    highlight: Optional[Highlight] = Field(default=None)
    highlight_id: StrObjectId
    time_to_highlight_seconds: Optional[int] = None

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['highlight'] = self.highlight.model_dump_json(serializer=SerializerType.API) if self.highlight else None
        return dump

class HighlightEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: HighlightData

    VALID_TYPES: ClassVar[set] = {
        EventType.HIGHLIGHT_CREATED,
        EventType.HIGHLIGHT_UPDATED,
        EventType.HIGHLIGHT_DELETED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: HighlightData, info: ValidationInfo):
        if info.data.get('type') != EventType.HIGHLIGHT_DELETED and not v.highlight:
            raise ValueError("highlight must be set for all events except HIGHLIGHT_DELETED")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump