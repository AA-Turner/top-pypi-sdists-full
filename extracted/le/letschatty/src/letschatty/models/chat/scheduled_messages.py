from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import model_validator, Field, field_validator
from zoneinfo import ZoneInfo
from enum import StrEnum
from letschatty.models.utils.types import StrObjectId
from ..messages.chatty_messages.base.message_draft import MessageDraft
from ..base_models.chatty_asset_model import ChattyAssetModel
from ..utils.types.message_types import MessageSubtype
from ..messages.chatty_messages.schema import ChattyContext
from ...models.utils.types.message_types import MessageType
from ..messages.message_templates.filled_data_from_frontend import FilledTemplateData, TemplateOrigin


class ScheduledMessageStatus(StrEnum):
    SCHEDULED = "scheduled" # Message is scheduled to be sent at a specific time
    ON_HOLD = "on_hold" # Message is on hold because the user has sent a message before the scheduled time and forced_send is set to False
    EXPIRED_ON_HOLD = "expired_on_hold" # Message is on hold because the scheduled time has passed and forced_send is set to False
    CANCELLED = "cancelled" # Message was cancelled and will not be sent
    SENT = "sent" # Message was sent to the user

class ScheduledMessageSubtype(StrEnum):
    FREE_MESSAGE = "free_message" # Message is a free message and will be sent to the user
    TEMPLATE = "template" # Message is a template and will be sent to the user
    CONTINUOUS_CONVERSATION = "continuous_conversation" # Message will be sent to the user as part of a continuous conversation

class ScheduledMessages(ChattyAssetModel):
    active: bool = Field(default=True)
    scheduled_at: datetime
    messages: Optional[List[MessageDraft]] = None
    filled_template_data: Optional[FilledTemplateData] = None
    creator_id: StrObjectId
    status: Optional[ScheduledMessageStatus] = Field(default=ScheduledMessageStatus.SCHEDULED)
    forced_send: bool = Field(default=False)
    subtype: Optional[ScheduledMessageSubtype]

    @property
    def template_data(self) -> FilledTemplateData:
        if not self.subtype == ScheduledMessageSubtype.TEMPLATE:
            raise ValueError("Asking for template data on a non-template message")
        if not self.filled_template_data:
            raise ValueError("Filled template data is required for template messages")
        return self.filled_template_data

    @property
    def is_expired(self) -> bool:
        return self.scheduled_at < datetime.now(ZoneInfo("UTC"))

    def update_if_expired(self) -> ScheduledMessages:
        if self.is_expired and self.status == ScheduledMessageStatus.ON_HOLD:
            self.set_status(status=ScheduledMessageStatus.EXPIRED_ON_HOLD)
        return self

    @model_validator(mode='after')
    def first_message_is_text(self):
        """First message must be a text message if type is free_text"""
        if self.subtype == ScheduledMessageSubtype.FREE_MESSAGE or self.subtype == ScheduledMessageSubtype.CONTINUOUS_CONVERSATION:
            if not self.messages:
                raise ValueError("Messages are required")
            first_message = self.messages[0]
            if first_message.type != MessageType.TEXT:
                raise ValueError("First message must be a text message")
        elif self.subtype == ScheduledMessageSubtype.TEMPLATE:
            if not isinstance(self.filled_template_data, FilledTemplateData):
                raise ValueError("Filled template data is required for template messages")
        else:
            raise ValueError(f"Invalid subtype for first message check: {self.subtype}")
        return self

    @model_validator(mode='after')
    def set_context_and_subtype_on_messages(self):
        if self.messages and (self.subtype == ScheduledMessageSubtype.FREE_MESSAGE or self.subtype == ScheduledMessageSubtype.CONTINUOUS_CONVERSATION):
            for message in self.messages:
                message.context = ChattyContext(scheduled_messages_id=self.id)
                message.subtype = MessageSubtype.SCHEDULED_MESSAGE
        elif self.filled_template_data and self.subtype == ScheduledMessageSubtype.TEMPLATE:
            self.filled_template_data.origin = TemplateOrigin.FROM_SCHEDULED_MESSAGES
            self.filled_template_data.scheduled_messages_id = self.id
        else:
            raise ValueError(f"Invalid subtype for shceduled messages: {self.subtype}")
        return self

    def set_status(self, status: ScheduledMessageStatus):
        if status == ScheduledMessageStatus.CANCELLED:
            self.active = False
        elif status == ScheduledMessageStatus.EXPIRED_ON_HOLD:
            self.active = True
        elif status == ScheduledMessageStatus.ON_HOLD:
            self.active = True
        elif status == ScheduledMessageStatus.SCHEDULED:
            self.active = True
        elif status == ScheduledMessageStatus.SENT:
            self.active = False
        else:
            raise ValueError(f"Invalid status: {status}")
        self.status = status

