"""El resumen de los mensajes de un chat: qué cambia en `chats` cuando entra o sale un mensaje.

Es lógica pura, sin base: `after(message)` dice cómo queda el resumen después de un mensaje y
`from_messages` lo rearma desde el historial (para reparar un resumen o para migrar). La
persistencia aplica exactamente estas reglas con una guarda «sólo si es más nuevo», así que un
mensaje viejo (historial importado de coexistence) nunca hace retroceder el resumen.

Reglas, las mismas que tenían las `@property` de `Chat` que recorrían los mensajes:

- `last_message`: el último mensaje que no es nota del sistema.
- `last_incoming_message`: el último del cliente, sin contar historial importado
  (`COEXISTENCE_IMPORT`), que no es actividad y no abre ventanas.
- `free_conversation_expire_date`: 24 h desde el último entrante que abre ventana: uno que llegó a
  un número que la cuenta ya no usa (5A) es actividad pero no abre ventana en el número actual.
- `free_template_window_expire_date`: 7 días desde el último entrante que llegó desde un anuncio
  (la ventana gratuita de Meta para Click-to-WhatsApp; eran 72 h hasta el 28-sep-2026).
- `last_outgoing_message`: el último que salió, sin notas del sistema.
- `first_outgoing_message_at`: el primero que salió. Vacío = nunca respondimos, que es lo que
  `is_first_message` calculaba recorriendo todo el historial.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

from ..messages.chatty_messages import ChattyMessage
from ..utils import Status
from ..utils.types.message_types import MessageSubtype, MessageType
from .message_summary import (
    IncomingMessageSummary,
    MessageSummary,
    OutgoingMessageSummary,
    _as_utc,
)

FREE_CONVERSATION_WINDOW = timedelta(hours=24)
FREE_TEMPLATE_WINDOW = timedelta(days=7)

#: Los campos del resumen, en `chats`. Los escribe sólo el escritor de mensajes.
SUMMARY_FIELDS = (
    "last_message",
    "last_message_timestamp",
    "last_incoming_message",
    "last_incoming_message_timestamp",
    "last_outgoing_message",
    "first_outgoing_message_at",
    "free_conversation_expire_date",
    "free_template_window_expire_date",
)


def counts_as_incoming_activity(message: ChattyMessage) -> bool:
    """Un mensaje del cliente que cuenta para las ventanas: no historial importado."""
    return (
        message.is_incoming_message
        and message.type != MessageType.CENTRAL
        and message.subtype != MessageSubtype.COEXISTENCE_IMPORT
    )


def opens_window(message: ChattyMessage) -> bool:
    """Un entrante que abre las ventanas de 24 h y de anuncio. No las abre el que llegó a un
    número anterior de la cuenta (5A): la respuesta sale por el número actual."""
    return counts_as_incoming_activity(message) and not message.context.received_on_previous_number


def _is_newer(candidate: datetime, current: Optional[datetime]) -> bool:
    return current is None or candidate >= current


class ChatSummary(BaseModel):
    """Los campos de resumen de un chat, como valor."""
    last_message: Optional[MessageSummary] = Field(default=None)
    last_message_timestamp: Optional[datetime] = Field(default=None)
    last_incoming_message: Optional[IncomingMessageSummary] = Field(default=None)
    last_incoming_message_timestamp: Optional[datetime] = Field(default=None)
    last_outgoing_message: Optional[OutgoingMessageSummary] = Field(default=None)
    first_outgoing_message_at: Optional[datetime] = Field(default=None)
    free_conversation_expire_date: Optional[datetime] = Field(default=None)
    free_template_window_expire_date: Optional[datetime] = Field(default=None)

    @classmethod
    def from_messages(cls, messages: Iterable[ChattyMessage]) -> "ChatSummary":
        """El resumen rearmado desde el historial, en orden cronológico."""
        summary = cls()
        for message in sorted(messages, key=lambda m: _as_utc(m.created_at)):
            summary = summary.after(message)
        return summary

    def after(self, message: ChattyMessage) -> "ChatSummary":
        """Cómo queda el resumen después de este mensaje. Un mensaje más viejo no lo hace retroceder."""
        created_at = _as_utc(message.created_at)
        assert created_at is not None
        updates: Dict[str, Any] = {}

        if message.type != MessageType.CENTRAL and _is_newer(created_at, self.last_message_timestamp):
            updates["last_message"] = MessageSummary.from_message(message)
            updates["last_message_timestamp"] = created_at

        if counts_as_incoming_activity(message) and _is_newer(created_at, self.last_incoming_message_timestamp):
            updates["last_incoming_message"] = IncomingMessageSummary.from_message(message)
            updates["last_incoming_message_timestamp"] = created_at
            if opens_window(message):
                updates["free_conversation_expire_date"] = created_at + FREE_CONVERSATION_WINDOW
                if not message.referral.is_default:
                    updates["free_template_window_expire_date"] = created_at + FREE_TEMPLATE_WINDOW

        if message.is_outgoing:
            current_outgoing_at = self.last_outgoing_message.created_at if self.last_outgoing_message else None
            if _is_newer(created_at, current_outgoing_at):
                updates["last_outgoing_message"] = OutgoingMessageSummary.from_message(message)
            if self.first_outgoing_message_at is None or created_at < self.first_outgoing_message_at:
                updates["first_outgoing_message_at"] = created_at

        return self.model_copy(update=updates)

    def with_status(self, message_id: str, status: Status) -> "ChatSummary":
        """El resumen después de un cambio de estado (✓✓) del mensaje `message_id`."""
        updates: Dict[str, Any] = {}
        if self.last_message and self.last_message.id == message_id:
            updates["last_message"] = self.last_message.model_copy(update={"status": status})
        if self.last_outgoing_message and self.last_outgoing_message.id == message_id:
            updates["last_outgoing_message"] = self.last_outgoing_message.model_copy(update={"status": status})
        return self.model_copy(update=updates)

    def to_document(self) -> Dict[str, Any]:
        """Los campos para `chats`, con las fechas como fecha. Las claves van siempre, aunque vacías:
        `preview_service` las lee con `doc[...]` y una clave que falta saca el chat de la bandeja."""
        return {
            "last_message": self.last_message.to_document() if self.last_message else None,
            "last_message_timestamp": self.last_message_timestamp,
            "last_incoming_message": self.last_incoming_message.to_document() if self.last_incoming_message else None,
            "last_incoming_message_timestamp": self.last_incoming_message_timestamp,
            "last_outgoing_message": self.last_outgoing_message.to_document() if self.last_outgoing_message else None,
            "first_outgoing_message_at": self.first_outgoing_message_at,
            "free_conversation_expire_date": self.free_conversation_expire_date,
            "free_template_window_expire_date": self.free_template_window_expire_date,
        }


def utc_now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))
