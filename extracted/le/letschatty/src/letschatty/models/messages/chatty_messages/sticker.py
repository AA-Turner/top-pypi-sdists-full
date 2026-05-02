from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentSticker

class StickerMessage(Message):
    type: MessageType = MessageType.STICKER
    content: ChattyContentSticker