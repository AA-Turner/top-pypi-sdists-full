from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentImage

class ImageMessage(Message):
    type: MessageType = MessageType.IMAGE
    content: ChattyContentImage