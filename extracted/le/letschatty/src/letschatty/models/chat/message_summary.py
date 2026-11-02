"""Resúmenes de mensajes que el chat guarda para no tener que recorrer sus mensajes.

Antes eran `@property` de `Chat` que recorrían `messages`. Con los mensajes en
`chat_messages`, cada lector que necesitaba «el último mensaje» o «el último entrante» habría
tenido que cargar el historial. Son campos chicos, guardados en `chats`, que escribe el
escritor de mensajes en la misma pasada que el mensaje (ver `ChatSummary`).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator

from ..messages.chatty_messages import ChattyMessage
from ..utils.types.message_types import MessageSubtype, MessageType
from ..utils import Status
from letschatty.services.messages_helpers import MessageTextOrCaptionOrPreview

#: Tope del texto del último mensaje. La bandeja muestra una línea; el tope sólo evita que un
#: mensaje enorme infle el documento que se lee en cada listado.
PREVIEW_MAX_CHARS = 500

_UTC = ZoneInfo("UTC")


def _as_utc(value: Optional[datetime]) -> Optional[datetime]:
    """Mongo devuelve las fechas sin zona: se leen como UTC, nunca como hora local."""
    if value is None:
        return None
    return value.replace(tzinfo=_UTC) if value.tzinfo is None else value.astimezone(_UTC)


class _SummaryBase(BaseModel):
    id: str
    created_at: datetime

    @field_validator("created_at", mode="after")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return _as_utc(value)  # type: ignore[return-value]

    def to_document(self) -> Dict[str, Any]:
        """Para Mongo: la fecha como fecha, no como texto (si no, las queries de rango no la ven)."""
        document = self.model_dump(mode="json")
        document["created_at"] = self.created_at
        return document


class MessageSummary(_SummaryBase):
    """El último mensaje del chat, sin notas del sistema: lo que muestran la bandeja y los lectores.

    Conserva las claves que ya leen los consumidores sobre el documento crudo
    (`is_incoming_message`, `status`, `sent_by`, `subtype`, `context.template_name` como
    `template_name`, `context.workflow_id` como `workflow_id`). El contenido completo no
    viaja: sólo `preview`, el texto o la descripción que muestra la bandeja, y `caption`, la
    leyenda de una foto, video o documento (la bandeja no la muestra, pero los lectores sí la
    leían del mensaje entero: una pregunta de precio o un «ya pagué» viaja en la leyenda).
    """
    type: MessageType
    subtype: MessageSubtype = Field(default=MessageSubtype.NONE)
    is_incoming_message: bool
    preview: str = Field(default="")
    status: Optional[Status] = Field(default=None)
    sent_by: Optional[str] = Field(default=None)
    template_name: Optional[str] = Field(default=None)
    workflow_id: Optional[str] = Field(default=None)
    caption: Optional[str] = Field(default=None)

    @classmethod
    def from_message(cls, message: ChattyMessage) -> "MessageSummary":
        return cls(
            id=message.id,
            created_at=message.created_at,
            type=message.type,
            subtype=message.subtype,
            is_incoming_message=message.is_incoming_message,
            preview=MessageTextOrCaptionOrPreview.get_content_preview(message_content=message.content)[:PREVIEW_MAX_CHARS],
            status=message.status,
            sent_by=message.sent_by,
            template_name=message.context.template_name,
            workflow_id=message.context.workflow_id,
            caption=(getattr(message.content, "caption", None) or None) and message.content.caption[:PREVIEW_MAX_CHARS],
        )

    @property
    def is_outgoing(self) -> bool:
        return not self.is_incoming_message and self.type != MessageType.CENTRAL

    @property
    def is_incoming(self) -> bool:
        return self.is_incoming_message

    def old_format(self) -> Dict[str, Any]:
        """La forma que leen la web y la app en las previews (`{is_incoming, type, content, datetime, status}`)."""
        return {
            "is_incoming": self.is_incoming_message,
            "type": self.type.value,
            "content": self.preview,
            "datetime": self.created_at.isoformat(),
            # CHAT-214: las notas del sistema no muestran tilde.
            "status": self.status.value if self.status and self.type != MessageType.CENTRAL else None,
        }


class IncomingMessageSummary(_SummaryBase):
    """El último mensaje del cliente (sin historial importado). Lo leen los acuses de lectura y copilot."""

    @classmethod
    def from_message(cls, message: ChattyMessage) -> "IncomingMessageSummary":
        return cls(id=message.id, created_at=message.created_at)


class OutgoingMessageSummary(_SummaryBase):
    """El último mensaje que salió (sin notas del sistema). Lo leen las condiciones de copilot y la
    coexistence de api-chatty, que pregunta si salió desde la app de WhatsApp (`subtype`
    `coexistence_echo`). Hasta 0.4.x `Chat.last_outgoing_message` devolvía el mensaje entero; 0.5.0
    lo cambió por este resumen sin `subtype` y esa lectura fallaba en cada entrante de una empresa
    con coexistence (prod, 6-oct-2026). Un resumen guardado sin `subtype` se lee como `NONE`."""
    subtype: MessageSubtype = Field(default=MessageSubtype.NONE)
    status: Optional[Status] = Field(default=None)
    sent_by: Optional[str] = Field(default=None)

    @classmethod
    def from_message(cls, message: ChattyMessage) -> "OutgoingMessageSummary":
        return cls(id=message.id, created_at=message.created_at, subtype=message.subtype,
                   status=message.status, sent_by=message.sent_by)
