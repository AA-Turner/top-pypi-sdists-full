from __future__ import annotations
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import model_validator, Field, field_validator
from zoneinfo import ZoneInfo
from enum import StrEnum
from ...models.utils.types import StrObjectId
from ..messages.chatty_messages.base.message_draft import MessageDraft
from ..base_models.chatty_asset_model import ChattyAssetModel
from ..utils.types.message_types import MessageSubtype
from ..messages.chatty_messages.schema import ChattyContext
from ...models.utils.types.message_types import MessageType

class CallToActionCC(StrEnum):
    GET_CC_MESSAGES = "get_cc_messages"
    AGENT_FORCE_SEND = "agent_force_send"

class ContinuousConversationStatus(StrEnum):
    APPROVED = "approved" # User accepted the CC request
    REJECTED = "rejected" # User rejected the CC request
    CANCELLED = "cancelled" # Agent canceled the CC request
    EXPIRED = "expired" # CC request expired without response
    OTHER_ANSWER = "other_answer" # User sent non-standard response
    FAILED = "failed" # CC request failed because template couldn't be send
    CREATED = "created" # CC request created
    REQUEST_SENT = "request_sent" # CC request sent to the user
    FORCED_SENT = "forced_sent" # CC request was forced to be sent

class ContinuousConversation(ChattyAssetModel):
    template_message_waid: Optional[str] = None
    status: Optional[ContinuousConversationStatus] = Field(default=ContinuousConversationStatus.CREATED)
    active: bool = Field(default=True)
    expires_at: datetime = Field(default=datetime.now(ZoneInfo("UTC")) + timedelta(days=10))
    messages: List[MessageDraft]
    creator_id: StrObjectId
    forced_send: bool = Field(default=False)
    calls_to_action: List[CallToActionCC] = Field(default=[])

    @property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(ZoneInfo("UTC"))

    @field_validator("messages")
    @classmethod
    def at_least_one_message(cls, v: List[MessageDraft]):
        """First message must be a text message"""
        if not v:
            raise ValueError("Messages are required")
        return v

    @model_validator(mode='after')
    def set_context_and_subtype_on_messages(self):
        for message in self.messages:
            if message.context is None:
                message.context = ChattyContext(continuous_conversation_id=self.id)
            else:
                message.context.continuous_conversation_id = self.id
            message.subtype = MessageSubtype.CONTINUOUS_CONVERSATION
        return self

    def append_messages(self, messages: List[MessageDraft]):
        for message in messages:
            if message.context is None:
                message.context = ChattyContext(continuous_conversation_id=self.id)
            else:
                message.context.continuous_conversation_id = self.id
            message.subtype = MessageSubtype.CONTINUOUS_CONVERSATION
            self.messages.append(message)
        return self


    def set_status(self, status: ContinuousConversationStatus):
        self.status = status
        if status == ContinuousConversationStatus.REQUEST_SENT:
            self.calls_to_action = []
        elif status == ContinuousConversationStatus.FORCED_SENT:
            self.calls_to_action = []
            self.active = False
        elif status == ContinuousConversationStatus.APPROVED:
            self.calls_to_action = []
            self.active = False
        elif status == ContinuousConversationStatus.REJECTED:
            self.calls_to_action = [CallToActionCC.GET_CC_MESSAGES]
            self.active = False
        elif status == ContinuousConversationStatus.CANCELLED:
            self.calls_to_action = [CallToActionCC.GET_CC_MESSAGES]
            self.active = False
        elif status == ContinuousConversationStatus.FAILED:
            self.calls_to_action = [CallToActionCC.GET_CC_MESSAGES]
            self.active = False
        elif status == ContinuousConversationStatus.OTHER_ANSWER:
            self.calls_to_action = [CallToActionCC.GET_CC_MESSAGES, CallToActionCC.AGENT_FORCE_SEND]
            self.active = False
        elif status == ContinuousConversationStatus.CREATED:
            self.calls_to_action = []
            self.active = True
        elif status == ContinuousConversationStatus.EXPIRED:
            self.calls_to_action = [CallToActionCC.GET_CC_MESSAGES, CallToActionCC.AGENT_FORCE_SEND]
            self.active = False
        return self
