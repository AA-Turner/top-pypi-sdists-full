from typing import ClassVar, Optional
from pydantic import Field, field_validator, ValidationInfo
from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....utils.types.identifier import StrObjectId
from ....company.CRM.funnel import ClientFunnel, StageTransition
import json

class FunnelEventData(CustomerEventData):
    funnel_id: StrObjectId
    funnel_stage_transition: StageTransition
    time_in_funnel_seconds: Optional[int] = None

class ChatFunnelEvent(Event):
    """Event for tracking chat funnel stage transitions"""
    data: FunnelEventData

    # Define valid event types for this event class
    VALID_TYPES: ClassVar[set] = {
        EventType.CHAT_FUNNEL_UPDATED,
        EventType.CHAT_FUNNEL_STARTED,
        EventType.CHAT_FUNNEL_COMPLETED,
        EventType.CHAT_FUNNEL_ABANDONED
    }


    @field_validator('data')
    def validate_data_fields(cls, v: FunnelEventData, info: ValidationInfo):
        """Validate that appropriate fields are set based on event type"""
        if info.data.get('type') == EventType.CHAT_FUNNEL_UPDATED and v.time_in_funnel_seconds is None:
            raise ValueError("time_in_funnel_seconds must be set for CHAT_FUNNEL_UPDATED events")
        if info.data.get('type') == EventType.CHAT_FUNNEL_UPDATED and v.funnel_stage_transition.time_in_previous_stage_seconds is None:
            raise ValueError("time_in_previous_stage_seconds must be set for CHAT_FUNNEL_UPDATED events")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump