from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentVideo

class VideoMessage(Message):
    type: MessageType = MessageType.VIDEO
    content: ChattyContentVideo