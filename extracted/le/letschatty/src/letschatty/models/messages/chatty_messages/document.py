from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentDocument

class DocumentMessage(Message):
    type: MessageType = MessageType.DOCUMENT
    content: ChattyContentDocument