from pydantic import BaseModel, Field
from ....utils.types.identifier import StrObjectId
from typing import Optional
from .chat_context import ChatContext
from ....utils.types.executor_types import ExecutorType
from ....company.assets.users.agent_chats_snapshot import AgentChatsSnapshot
from ....company.company_chats_snapshot import CompanyChatsSnapshot
from ..base import EventData
import json

class CustomerEventData(EventData):
    company_phone_number_id: str
    company_waba_id: str
    chat_id: Optional[StrObjectId] = Field(default=None)
    client_phone_number : Optional[str] = Field(default=None)
    client_email : Optional[str] = Field(default=None)
    client_country : Optional[str] = Field(default=None)
    client_name : Optional[str] = Field(default=None)
    ctwa_clid : Optional[str] = Field(default=None)
    fb_clid : Optional[str] = Field(default=None)
    gclid : Optional[str] = Field(default=None)
    client_ip_address : Optional[str] = Field(default=None)
    client_user_agent : Optional[str] = Field(default=None)
    client_external_id : Optional[str] = Field(default=None)
    executor_type: ExecutorType
    executor_id: StrObjectId
    chat_context: Optional[ChatContext] = Field(default=None)
    agent_snapshot: Optional[AgentChatsSnapshot] = Field(default=None)
    company_snapshot: Optional[CompanyChatsSnapshot] = Field(default=None)

    @property
    def message_group_id(self) -> str:
        return f"chat-{self.chat_id}"
