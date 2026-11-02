from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema.chatty_content.content_interactive import ChattyContentInteractive

class InteractiveMessage(Message):
    type: MessageType = MessageType.INTERACTIVE
    content: ChattyContentInteractive
