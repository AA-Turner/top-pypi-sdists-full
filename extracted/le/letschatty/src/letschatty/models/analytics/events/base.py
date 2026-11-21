from pydantic import BaseModel, Field, ConfigDict, field_validator
from bson import ObjectId
from datetime import datetime
from typing import Optional
from ...utils.types.identifier import StrObjectId
from zoneinfo import ZoneInfo
from .event_types import EventType
import json

class EventData(BaseModel):
    pass

    @property
    def message_group_id(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")

class Event(BaseModel):
    """An analytics event.

    `model_dump_json()` in the subclasses returns a **dict**, not a string (since a327c755, letschatty .49, 2025-06-19): the dict
    carries `data` nested as a JSON string, which is the shape the analytics consumers read. Whoever publishes it serializes the
    dict once, e.g. api-chatty's `events_manager` sends `Detail=json.dumps(event.model_dump_json())`; serializing a string again
    is the double-encoded `Detail` EventBridge rejects (`docs/eventbridge-publishing.md` in api-chatty). The name is kept because
    other repos (lambdas, cintia) call it."""
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    specversion: str = Field(description="The version of the package")
    type: EventType
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(tz=ZoneInfo("UTC")))
    time: datetime = Field(description= "The timestamp of the event when it happened")
    data: EventData
    source: str = Field(description="The notifier that triggered the event, e.g. 'chatty_api.mobile', 'chatty_api.webapp'chatty_copilot'. Eventually could be 'manychat' or whatever source")
    company_id: StrObjectId
    frozen_company_name: str = Field(description="Used to identify the company with a readable name")
    trace_id: Optional[str] = Field(default=None, description="Trace ID for tracking event flows across the system")

    model_config = ConfigDict(
        exclude_none=True)

    @property
    def message_group_id(self) -> str:
        return self.data.message_group_id

    @field_validator('type')
    def validate_event_type(cls, value):
        """Ensure only valid event types are used"""
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid event type for Event: {value}. "
                           f"Must be one of: {', '.join(str(t) for t in cls.VALID_TYPES)}")
        return value
