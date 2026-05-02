from __future__ import annotations
from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentCentral


class CentralNotification(Message):
    type: MessageType = MessageType.CENTRAL
    content: ChattyContentCentral