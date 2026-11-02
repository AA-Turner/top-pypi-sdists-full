from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentReaction

class ReactionMessage(Message):
    type: MessageType = MessageType.REACTION
    content: ChattyContentReaction