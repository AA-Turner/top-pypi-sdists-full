from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....utils.types.identifier import StrObjectId
from pydantic import Field, field_validator
from typing import Optional, ClassVar
from ....company.assets.contact_point import ContactPoint
from ....utils.types.serializer_type import SerializerType
import json

class ContactPointData(CustomerEventData):
    contact_point_id: StrObjectId
    source_id: Optional[StrObjectId] = Field(default=None)
    new_chat : bool
    matched: bool
    wamid: Optional[str] = Field(default=None)
    time_from_request_to_match_seconds : Optional[int] = Field(default=None)
    topic_id : Optional[StrObjectId] = Field(default=None)
    contact_point: Optional[ContactPoint] = Field(default=None)

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['contact_point'] = self.contact_point.model_dump_json(serializer=SerializerType.API) if self.contact_point else None
        return dump

class ContactPointEvent(Event):
    """Event for contact point operations"""
    data: ContactPointData

    # Define valid event types for this event class
    VALID_TYPES: ClassVar[set] = {
        EventType.CONTACT_POINT_CREATED,
        EventType.CONTACT_POINT_UPDATED,
        EventType.CONTACT_POINT_DELETED
    }

    @field_validator('type')
    def validate_event_type(cls, value):
        """Ensure only valid contact point event types are used"""
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid event type for ContactPointEvent: {value}. "
                           f"Must be one of: {', '.join(str(t) for t in cls.VALID_TYPES)}")
        return value

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump