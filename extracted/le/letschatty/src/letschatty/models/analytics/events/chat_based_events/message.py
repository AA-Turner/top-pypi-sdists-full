
from ....messages.chatty_messages import ChattyMessage
from ....utils.types import Status
from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....utils.types.executor_types import ExecutorType
from ....utils.types.identifier import StrObjectId
from typing import Optional, ClassVar
from pydantic import Field, field_validator, ValidationInfo
import json
from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent import N8NWorkspaceAgentType

class MessageData(CustomerEventData):
    wamid : str
    message : Optional[ChattyMessage] = None
    new_status : Optional[Status] = None

class MessageEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: MessageData
    webhook_for_agent_type : Optional[N8NWorkspaceAgentType] = Field(default=None, description="The webhook to redirect the message to")

    VALID_TYPES: ClassVar[set] = {
        EventType.MESSAGE_RECEIVED,
        EventType.MESSAGE_SENT,
        EventType.MESSAGE_STATUS_UPDATED
    }

    @field_validator('data')
    def validate_data_fields(cls, v: MessageData, info: ValidationInfo):
        if info.data.get('type') in [EventType.MESSAGE_RECEIVED, EventType.MESSAGE_SENT] and not v.message:
            raise ValueError("message must be set for MESSAGE_RECEIVED and MESSAGE_SENT events")
        if info.data.get('type') == EventType.MESSAGE_STATUS_UPDATED and not v.new_status:
            raise ValueError("new_status must be set for MESSAGE_STATUS_UPDATED events")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump