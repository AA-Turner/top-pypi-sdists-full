"""El update de `chats` que aplica un mensaje al resumen, con guarda «sólo si es más nuevo».

Es la versión persistente de `ChatSummary.after`, en un único update con pipeline: cada campo
compara la fecha del mensaje con la guardada y se queda con el más nuevo. Así no hace falta leer
el chat, ni lock, y un mensaje viejo (historial importado) nunca hace retroceder el resumen.

Los valores van envueltos en `$literal`: un texto que empieza con `$` («$100 de descuento»)
sería, si no, una ruta de campo.
"""
from datetime import datetime
from typing import Any, Dict, List

from ....models.chat.chat_summary import (
    FREE_CONVERSATION_WINDOW, FREE_TEMPLATE_WINDOW, counts_as_incoming_activity, opens_window,
)
from ....models.chat.message_summary import (
    IncomingMessageSummary, MessageSummary, OutgoingMessageSummary, _as_utc,
)
from ....models.messages.chatty_messages import ChattyMessage
from ....models.utils.types.message_types import MessageType


def _is_newer(stored_path: str, candidate: datetime) -> Dict[str, Any]:
    """Si `candidate` es igual o más nuevo que lo guardado. Un campo vacío o ausente siempre pierde."""
    return {"$lte": [{"$ifNull": [f"${stored_path}", None]}, candidate]}


def _pick(condition: Dict[str, Any], new_value: Any, field: str) -> Dict[str, Any]:
    return {"$cond": [condition, {"$literal": new_value}, f"${field}"]}


def summary_update_pipeline(message: ChattyMessage, now: datetime) -> List[Dict[str, Any]]:
    created_at = _as_utc(message.created_at)
    fields: Dict[str, Any] = {"updated_at": now}

    if message.type != MessageType.CENTRAL:
        newer = _is_newer("last_message_timestamp", created_at)
        fields["last_message"] = _pick(newer, MessageSummary.from_message(message).to_document(), "last_message")
        fields["last_message_timestamp"] = _pick(newer, created_at, "last_message_timestamp")

    if counts_as_incoming_activity(message):
        newer = _is_newer("last_incoming_message_timestamp", created_at)
        fields["last_incoming_message"] = _pick(newer, IncomingMessageSummary.from_message(message).to_document(), "last_incoming_message")
        fields["last_incoming_message_timestamp"] = _pick(newer, created_at, "last_incoming_message_timestamp")
        if opens_window(message):
            fields["free_conversation_expire_date"] = _pick(newer, created_at + FREE_CONVERSATION_WINDOW, "free_conversation_expire_date")
            if not message.referral.is_default:
                fields["free_template_window_expire_date"] = _pick(newer, created_at + FREE_TEMPLATE_WINDOW, "free_template_window_expire_date")

    if message.is_outgoing:
        newer = _is_newer("last_outgoing_message.created_at", created_at)
        fields["last_outgoing_message"] = _pick(newer, OutgoingMessageSummary.from_message(message).to_document(), "last_outgoing_message")
        earlier = {"$or": [
            {"$eq": [{"$ifNull": ["$first_outgoing_message_at", None]}, None]},
            {"$lt": [created_at, "$first_outgoing_message_at"]},
        ]}
        fields["first_outgoing_message_at"] = _pick(earlier, created_at, "first_outgoing_message_at")

    return [{"$set": fields}]
