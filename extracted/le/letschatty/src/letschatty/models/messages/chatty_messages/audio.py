from .base.message_base import Message
from .schema import ChattyContentAudio
from ...utils.types.message_types import MessageType

class AudioMessage(Message):
    type: MessageType = MessageType.AUDIO
    content: ChattyContentAudio