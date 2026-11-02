from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentContacts
from ...utils.types.serializer_type import SerializerType
import json
from typing import Dict, Any

class ContactMessage(Message):
    type: MessageType = MessageType.CONTACT
    content: ChattyContentContacts

