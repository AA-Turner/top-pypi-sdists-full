"""Un bloque de mensajes de un chat: un documento de `chat_messages`.

Los mensajes de un chat se guardan de a `BUCKET_SIZE` por documento, numerados por `seq`.
Abrir un chat lee los últimos bloques hasta juntar la ventana que pide la web; cambiar un
mensaje (✓✓, edición, revocación) toca sólo su bloque. Ver `ChatMessagesCollection` para cómo
se escriben sin depender del lock por chat.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..messages.chatty_messages import ChattyMessage, ChattyMessageField
from ..utils.types.identifier import StrObjectId
from ..utils.types.message_types import MessageSubtype, MessageType
from .message_summary import _as_utc

#: Mensajes por bloque. Decide el costo de cada ✓✓ (se reescribe el bloque) y cuántos documentos
#: se leen para abrir un chat (la ventana de hoy es de 300 mensajes: 6 bloques).
BUCKET_SIZE = 50


def counts_as_visible(message: ChattyMessage) -> bool:
    """Si el mensaje cuenta para la paginación del chat.

    Las reacciones se muestran pegadas a su mensaje y las plantillas de una conversación
    continua las representa la conversación continua: ninguna de las dos es una burbuja propia,
    así que no cuentan para `total_messages` (misma regla que `dump_chat_for_frontend`).
    """
    if message.type == MessageType.REACTION:
        return False
    if message.subtype == MessageSubtype.TEMPLATE and message.context.continuous_conversation_id is not None:
        return False
    return True


def message_to_document(message: ChattyMessage) -> Dict[str, Any]:
    """Un mensaje como se guarda hoy en Mongo: la misma forma que tenía en `chats.messages`."""
    return message.model_dump(by_alias=True, mode="json")


class ChatMessagesBucket(BaseModel):
    id: StrObjectId = Field(alias="_id", default_factory=lambda: str(ObjectId()))
    company_id: StrObjectId
    chat_id: StrObjectId
    seq: int = Field(description="Orden del bloque dentro del chat. Negativo para historial importado anterior al primer bloque")
    count: int = Field(ge=0)
    visible_count: int = Field(ge=0)
    first_at: datetime
    last_at: datetime
    messages: List[ChattyMessageField] = Field(default_factory=list)

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    @field_validator("first_at", "last_at", mode="after")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return _as_utc(value)  # type: ignore[return-value]

    @classmethod
    def new(cls, company_id: StrObjectId, chat_id: StrObjectId, seq: int, messages: List[ChattyMessage]) -> "ChatMessagesBucket":
        if not messages:
            raise ValueError("Un bloque se crea con al menos un mensaje")
        ordered = sorted(messages, key=lambda m: _as_utc(m.created_at))
        return cls(
            company_id=company_id,
            chat_id=chat_id,
            seq=seq,
            count=len(ordered),
            visible_count=sum(1 for m in ordered if counts_as_visible(m)),
            first_at=ordered[0].created_at,
            last_at=ordered[-1].created_at,
            messages=ordered,
        )

    def to_document(self) -> Dict[str, Any]:
        return {
            "_id": ObjectId(self.id),
            "company_id": self.company_id,
            "chat_id": self.chat_id,
            "seq": self.seq,
            "count": self.count,
            "visible_count": self.visible_count,
            "first_at": self.first_at,
            "last_at": self.last_at,
            "messages": [message_to_document(m) for m in self.messages],
        }

    @classmethod
    def from_document(cls, document: Dict[str, Any]) -> "ChatMessagesBucket":
        from letschatty.services.factories.messages.chatty_message_factory import from_message_json

        data = dict(document)
        data["_id"] = str(data["_id"])
        data["messages"] = [from_message_json(m) for m in data.get("messages", [])]
        return cls(**data)
