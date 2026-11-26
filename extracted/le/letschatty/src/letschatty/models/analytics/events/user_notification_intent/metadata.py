from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field

from ....utils.types.identifier import StrObjectId
from ....push_notifications.enums import NotificationIntentType
from ....messages.chatty_messages import ChattyMessage


class ChatAssignedMetadata(BaseModel):
    intent: Literal[NotificationIntentType.CHAT_ASSIGNED] = (
        NotificationIntentType.CHAT_ASSIGNED
    )


class IncomingMessageMetadata(BaseModel):
    intent: Literal[NotificationIntentType.CHAT_MESSAGE_RECEIVED] = (
        NotificationIntentType.CHAT_MESSAGE_RECEIVED
    )
    message_id: str
    message: Optional[ChattyMessage] = Field(
        default=None,
        description="Message that triggered the notification. Optional for payload size.",
    )


class ChatEscalatedMetadata(BaseModel):
    intent: Literal[NotificationIntentType.CHAT_ESCALATED] = (
        NotificationIntentType.CHAT_ESCALATED
    )
    reason: str


class AsistenteRespuestaListaMetadata(BaseModel):
    """El asistente (Lucía, el chat lateral) terminó de responder. Sin campos extra: la
    conversación es el `chat_id` del evento."""

    intent: Literal[NotificationIntentType.ASISTENTE_RESPUESTA_LISTA] = (
        NotificationIntentType.ASISTENTE_RESPUESTA_LISTA
    )


NotificationIntentMetadata = Annotated[
    Union[
        ChatAssignedMetadata,
        IncomingMessageMetadata,
        ChatEscalatedMetadata,
        AsistenteRespuestaListaMetadata,
    ],
    Field(discriminator="intent"),
]
