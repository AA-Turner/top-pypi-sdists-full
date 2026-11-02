from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from typing import ClassVar, Optional
from ....utils.types.identifier import StrObjectId
from ....company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from pydantic import field_validator, ValidationInfo
from ....utils.types.serializer_type import SerializerType
import json

class ChattyAIChatData(CustomerEventData):
    chatty_ai_agent_id: StrObjectId
    chatty_ai_agent: ChattyAIAgent
    time_to_chatty_ai_agent_seconds: Optional[int] = None

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['chatty_ai_agent'] = self.chatty_ai_agent.model_dump_json(serializer=SerializerType.API) if self.chatty_ai_agent else None
        return dump

class ChattyAIChatEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: ChattyAIChatData

    VALID_TYPES: ClassVar[set] = {
        EventType.AI_AGENT_ASSIGNED_TO_CHAT,
        EventType.AI_AGENT_UPDATED_ON_CHAT,
        EventType.AI_AGENT_REMOVED_FROM_CHAT
    }


    @field_validator('data')
    def validate_data_fields(cls, v: ChattyAIChatData, info: ValidationInfo):
        if info.data.get('type') != EventType.AI_AGENT_REMOVED_FROM_CHAT and not v.chatty_ai_agent:
            raise ValueError("chatty_ai_agent must be set for all events except AI_AGENT_REMOVED_FROM_CHAT")
        return v

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump