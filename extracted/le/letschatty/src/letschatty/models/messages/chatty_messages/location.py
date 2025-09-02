from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentLocation

class LocationMessage(Message):
    type: MessageType = MessageType.LOCATION
    content: ChattyContentLocation