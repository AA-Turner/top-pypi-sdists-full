from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....utils.types.identifier import StrObjectId
from pydantic import Field, field_validator, ValidationInfo
from enum import StrEnum
from typing import Optional, ClassVar
from letschatty.models.chat.flow_link_state import ExecutionResult
import json

class WorkflowEventData(CustomerEventData):
    workflow_id: StrObjectId
    execution_result: ExecutionResult
    execution_time_seconds: Optional[float] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

class WorkflowEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: WorkflowEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.WORKFLOW_ASSIGNED,
        EventType.WORKFLOW_REMOVED,
        EventType.WORKFLOW_STATUS_UPDATED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: WorkflowEventData, info: ValidationInfo):
        if info.data.get('type') == EventType.WORKFLOW_STATUS_UPDATED and (not v.execution_result):
            raise ValueError("execution_result must be set for WORKFLOW_STATUS_UPDATED events")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump