from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentText

class TextMessage(Message):
    type: MessageType = MessageType.TEXT
    content: ChattyContentText