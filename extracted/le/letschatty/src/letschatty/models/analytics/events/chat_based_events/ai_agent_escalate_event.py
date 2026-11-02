from typing import ClassVar, Optional

from pydantic import Field

from ..base import Event, EventData
from ..event_types import EventType
from ....utils.types.identifier import StrObjectId


class AiAgentEscalateEventData(EventData):
    chat_id: StrObjectId
    reason: Optional[str] = None
    account_id: Optional[StrObjectId] = Field(default=None, description="The WhatsApp account of the chat (multi-account). None = default account / pre-migration chat. Same dimension as the other chat events' data.account_id")

    @property
    def message_group_id(self) -> str:
        return str(self.chat_id)


class AiAgentEscalateEvent(Event):
    data: AiAgentEscalateEventData

    VALID_TYPES: ClassVar[set] = {
        EventType.AI_AGENT_ESCALATE,
        EventType.AI_AGENT_UNESCALATE,
    }
