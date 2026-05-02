from typing import Optional

from ....utils.types.identifier import StrObjectId
from ....messages.chatty_messages import ChattyMessage
from .metadata import ChatAssignedMetadata, IncomingMessageMetadata, ChatEscalatedMetadata


def build_chat_assigned_metadata() -> ChatAssignedMetadata:
    return ChatAssignedMetadata()


def build_incoming_message_metadata(
    message_id: StrObjectId,
    message: Optional[ChattyMessage] = None,
) -> IncomingMessageMetadata:
    return IncomingMessageMetadata(message_id=message_id, message=message)


def build_chat_escalated_metadata(
    reason: str,
) -> ChatEscalatedMetadata:
    return ChatEscalatedMetadata(reason=reason)
