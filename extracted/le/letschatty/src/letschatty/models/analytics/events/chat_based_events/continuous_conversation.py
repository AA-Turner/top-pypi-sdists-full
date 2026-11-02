from typing import ClassVar, Optional
from pydantic import Field, field_validator, ValidationInfo
from ....utils.types.identifier import StrObjectId
from ..event_types import EventType
from ..base import Event
from .chat_based_event import CustomerEventData
from ....chat.continuous_conversation import ContinuousConversation, ContinuousConversationStatus
from ....utils.types.serializer_type import SerializerType
import json


class ContinuousConversationData(CustomerEventData):
    cc_id: StrObjectId
    continuous_conversation: Optional[ContinuousConversation] = Field(default=None)
    template_message_waid: Optional[str] = Field(default=None)
    status: Optional[ContinuousConversationStatus] = Field(default=None)

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['continuous_conversation'] = self.continuous_conversation.model_dump_json(serializer=SerializerType.API) if self.continuous_conversation else None
        return dump

class ContinuousConversationEvent(Event):
    """Event for continuous conversation operations"""
    data: ContinuousConversationData

    # Define valid event types for this event class
    VALID_TYPES: ClassVar[set] = {
        EventType.CONTINUOUS_CONVERSATION_CREATED,
        EventType.CONTINUOUS_CONVERSATION_UPDATED
    }

    @field_validator('type')
    def validate_event_type(cls, value):
        """Ensure only valid continuous conversation event types are used"""
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid event type for ContinuousConversationEvent: {value}. "
                           f"Must be one of: {', '.join(str(t) for t in cls.VALID_TYPES)}")
        return value

    @field_validator('data')
    def validate_data_fields(cls, v: ContinuousConversationData, info: ValidationInfo):
        if info.data.get('type') != EventType.CONTINUOUS_CONVERSATION_UPDATED and not v.continuous_conversation:
            raise ValueError("continuous_conversation must be set for all events except CONTINUOUS_CONVERSATION_UPDATED")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump