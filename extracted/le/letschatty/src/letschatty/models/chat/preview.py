from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from ..utils.types import StrObjectId
from ..messages.chatty_messages import ChattyMessage
from zoneinfo import ZoneInfo
from datetime import datetime
from .time_left import TimeLeft
from .scheduled_messages import ScheduledMessageStatus
from ..company.assets.tag import TagPreview
from typing import List, Optional
from .time_left import TimeLeft
from letschatty.services.messages_helpers import MessageTextOrCaptionOrPreview
from ...models.utils.definitions import Area
import json
import logging
from enum import StrEnum

logger = logging.getLogger("ChatPreviewModel")

class ChattyAiAgentStatus(StrEnum):
    ASSIGNED = "assigned"
    ESCALATED = "escalated"

class ClientPreview(BaseModel):
    name: str
    phone_number: str

class AgentPreview(BaseModel):
    name: str
    email: Optional[str] = Field(default=None)
    id: StrObjectId
    photo_url: Optional[str] = Field(default=None)

class ChatPreview(BaseModel):
    chat_id: StrObjectId
    area_status : Area
    agent : Optional[AgentPreview] = Field(default=None)
    client : ClientPreview
    last_message : Optional[ChattyMessage]
    is_read_status : bool
    free_conversation_expire_date : datetime
    free_template_window_expire_date : datetime
    starred : bool
    created_at : datetime
    scheduled_message : Optional[ScheduledMessageStatus] = Field(default=None)
    tags : Optional[List[TagPreview]] = Field(default=[])
    chatty_ai_agent_status : Optional[ChattyAiAgentStatus] = Field(default=None)
    @property
    def assigned_agent_id(self) -> Optional[StrObjectId]:
        if self.area_status != Area.WITH_AGENT:
            raise ValueError(f"Chat is not assigned to an agent: {self.chat_id} client: {self.client.name}")
        if self.agent is None:
            raise ValueError(f"Agent is not assigned to this chat: {self.chat_id} client: {self.client.name}")
        return self.agent.id

    def last_message_old_format(self) -> dict:
        if self.last_message is None:
            return {
                "is_incoming": False,
                "type": "text",
                "content": "No hay mensajes",
                "datetime": self.created_at.isoformat(),
            }
        return {
            "is_incoming": self.last_message.is_incoming_message,
            "type": self.last_message.type.value,
            "content": MessageTextOrCaptionOrPreview.get_content_preview(message_content=self.last_message.content),
            "datetime": self.last_message.created_at.isoformat(),
        }

    def model_dump(self) -> dict:
        dump = json.loads(super().model_dump_json())
        dump["last_message"] = self.last_message_old_format()
        logger.debug(f"self.free_conversation_expire_date: {self.free_conversation_expire_date}")
        logger.debug(f"self.free_template_window_expire_date: {self.free_template_window_expire_date}")
        dump["time_left"] = TimeLeft.get_time_left(
            time_left_for_free_conversation_seconds=(self.free_conversation_expire_date.replace(tzinfo=ZoneInfo("UTC")) - datetime.now(tz=ZoneInfo("UTC"))).total_seconds(),
            time_left_for_free_template_window_seconds=(self.free_template_window_expire_date.replace(tzinfo=ZoneInfo("UTC")) - datetime.now(tz=ZoneInfo("UTC"))).total_seconds()
        ).model_dump()
        logger.debug(f"dump['time_left']: {dump['time_left']}")
        return dump

