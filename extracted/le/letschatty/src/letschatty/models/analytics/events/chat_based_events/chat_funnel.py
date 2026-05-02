from typing import ClassVar, Optional
from pydantic import Field, field_validator, ValidationInfo
from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....utils.types.identifier import StrObjectId
from ....company.CRM.funnel import StageTransition
import json


class FunnelEventData(CustomerEventData):
    """
    Event data for chat funnel events.
    
    Fields required per event type:
    - STARTED: funnel_id, chat_funnel_id, stage_transition
    - STAGE_CHANGED: funnel_id, chat_funnel_id, stage_transition (with time_in_previous_stage_seconds)
    - COMPLETED: funnel_id, chat_funnel_id, time_in_funnel_seconds, time_in_last_stage_seconds
    - ABANDONED: funnel_id, chat_funnel_id, time_in_funnel_seconds, time_in_last_stage_seconds
    """
    funnel_id: StrObjectId = Field(description="The funnel the chat is in")
    chat_funnel_id: StrObjectId = Field(description="Reference to the ChatFunnel record")
    
    # For STARTED and STAGE_CHANGED events
    stage_transition: Optional[StageTransition] = Field(
        default=None,
        description="The stage transition details (for STARTED and STAGE_CHANGED)"
    )
    
    # For COMPLETED and ABANDONED events
    time_in_funnel_seconds: Optional[int] = Field(
        default=None,
        description="Total time spent in the funnel (for COMPLETED and ABANDONED)"
    )
    time_in_last_stage_seconds: Optional[int] = Field(
        default=None,
        description="Time spent in the last stage before completion/abandonment"
    )


class ChatFunnelEvent(Event):
    """
    Event for tracking chat funnel lifecycle.
    
    Events:
    - CHAT_FUNNEL_STARTED: Chat entered a funnel
    - CHAT_FUNNEL_STAGE_CHANGED: Chat moved between stages
    - CHAT_FUNNEL_COMPLETED: Chat completed the funnel
    - CHAT_FUNNEL_ABANDONED: Chat abandoned the funnel
    """
    data: FunnelEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.CHAT_FUNNEL_STARTED,
        EventType.CHAT_FUNNEL_STAGE_CHANGED,
        EventType.CHAT_FUNNEL_COMPLETED,
        EventType.CHAT_FUNNEL_ABANDONED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: FunnelEventData, info: ValidationInfo):
        """Validate that appropriate fields are set based on event type"""
        event_type = info.data.get('type')
        
        # STARTED: requires stage_transition
        if event_type == EventType.CHAT_FUNNEL_STARTED:
            if v.stage_transition is None:
                raise ValueError("stage_transition must be set for CHAT_FUNNEL_STARTED events")
        
        # STAGE_CHANGED: requires stage_transition with time_in_previous_stage_seconds
        elif event_type == EventType.CHAT_FUNNEL_STAGE_CHANGED:
            if v.stage_transition is None:
                raise ValueError("stage_transition must be set for CHAT_FUNNEL_STAGE_CHANGED events")
            if v.stage_transition.time_in_previous_stage_seconds is None:
                raise ValueError("time_in_previous_stage_seconds must be set in stage_transition for CHAT_FUNNEL_STAGE_CHANGED events")
        
        # COMPLETED: requires time metrics
        elif event_type == EventType.CHAT_FUNNEL_COMPLETED:
            if v.time_in_funnel_seconds is None:
                raise ValueError("time_in_funnel_seconds must be set for CHAT_FUNNEL_COMPLETED events")
            if v.time_in_last_stage_seconds is None:
                raise ValueError("time_in_last_stage_seconds must be set for CHAT_FUNNEL_COMPLETED events")
        
        # ABANDONED: requires time metrics
        elif event_type == EventType.CHAT_FUNNEL_ABANDONED:
            if v.time_in_funnel_seconds is None:
                raise ValueError("time_in_funnel_seconds must be set for CHAT_FUNNEL_ABANDONED events")
            if v.time_in_last_stage_seconds is None:
                raise ValueError("time_in_last_stage_seconds must be set for CHAT_FUNNEL_ABANDONED events")
        
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump
