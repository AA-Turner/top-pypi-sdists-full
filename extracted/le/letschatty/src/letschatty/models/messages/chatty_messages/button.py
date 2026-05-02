from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentButton

class ButtonMessage(Message):
    type: MessageType = MessageType.BUTTON
    content: ChattyContentButton