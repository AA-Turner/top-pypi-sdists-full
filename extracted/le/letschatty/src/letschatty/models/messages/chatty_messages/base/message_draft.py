from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator
from zoneinfo import ZoneInfo
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import StrEnum
from ....utils.types.message_types import MessageType, MessageSubtype
from ..schema import ChattyContent, ChattyContext, ChattyContentText, ChattyContentImage, ChattyContentVideo, ChattyContentDocument, ChattyContentSticker, ChattyContentAudio, ChattyContentContacts, ChattyContentLocation, ChattyContentCentral, ChattyContentReaction


class MessageDraft(BaseModel):
    """This class validates and represents the content of a message that's not yet instantiated.
    It's used to validate either a message request from the frontend, or the messages inside a ChattyResponse"""
    type: MessageType
    content: ChattyContent
    context: Optional[ChattyContext] = Field(default_factory=ChattyContext.default)
    subtype: Optional[MessageSubtype] = Field(default=MessageSubtype.NONE)
    is_incoming_message : bool = Field(default=False)

    @property
    def context_value(self) -> ChattyContext:
        if self.context is None:
            raise ValueError("Context is required")
        return self.context

    @property
    def subtype_value(self) -> MessageSubtype:
        if self.subtype is None:
            raise ValueError("Subtype is required")
        return self.subtype


    @field_validator('content', mode='before')
    def validate_content(cls, v, values: ValidationInfo):
        if isinstance(v,ChattyContent):
            return v
        message_type = values.data.get('type')
        message_type = MessageType(message_type)
        content_class = {
            MessageType.TEXT: ChattyContentText,
            MessageType.IMAGE: ChattyContentImage,
            MessageType.VIDEO: ChattyContentVideo,
            MessageType.DOCUMENT: ChattyContentDocument,
            MessageType.STICKER: ChattyContentSticker,
            MessageType.AUDIO: ChattyContentAudio,
            MessageType.CONTACT: ChattyContentContacts,
            MessageType.LOCATION: ChattyContentLocation,
            MessageType.CENTRAL: ChattyContentCentral,
            MessageType.REACTION: ChattyContentReaction,
        }.get(message_type)

        if content_class is None:
            raise ValueError(f"Invalid message type: {message_type} - valid types: {MessageType.values()}")

        return content_class(**v)

    @field_validator('context', mode='before')
    def validate_context(cls, v):
        if isinstance(v,ChattyContext):
            return v
        if v is not None:
            return ChattyContext(**v)
        return v

class SendMessagesFromAgentToChat(BaseModel):
    """Send messages from an agent to a chat"""
    messages: List[MessageDraft]
    scheduled_at: Optional[datetime] = Field(default=None, description="Leave None if the message is not scheduled and will be sent immediately, otherwise the message will be scheduled to be sent at the specified time") #
    forced_send: bool = Field(default=False, description="Control mechanism to send message anyway in determined situations, or to abort, for example if the user has sent a message before the scheduled time") #If True, the message will be sent immediately, otherwise it will be scheduled

    @model_validator(mode='after')
    def set_scheduled_at(self):
        if self.scheduled_at and self.scheduled_at < datetime.now(ZoneInfo("UTC")):
            raise ValueError("Scheduled at must be in the future")
        return self
