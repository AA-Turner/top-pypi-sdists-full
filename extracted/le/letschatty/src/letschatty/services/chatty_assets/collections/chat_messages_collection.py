"""Los mensajes de los chats, de a `BUCKET_SIZE` por documento (colección `chat_messages`).

**La escritura no cuenta con el lock por chat.** Hay muchos caminos que agregan mensajes fuera
del MessageProcessor (notas del sistema de cada editor, ecos, plantillas), así que dos
escritores pueden llegar a la vez al mismo chat. La seguridad la dan dos índices únicos y una
escritura condicional:

- `{chat_id, seq}` único: dos escritores que abren el bloque siguiente a la vez no crean dos.
- `{chat_id, messages.id}` único: el mismo wamid no queda en dos bloques. Dentro del mismo
  bloque lo impide la condición `messages.id != id` del `$push`.
- El `$push` sólo entra si el último bloque tiene lugar (`count < BUCKET_SIZE`). Si otro
  escritor lo llenó, se reintenta.

Un mensaje viejo (historial importado de coexistence) no va al último bloque: va a bloques
anteriores al primero (`seq` negativo) o se intercala en el bloque cuyo rango lo contiene, que
entonces puede pasar de 50. Así el orden de los bloques sigue siendo cronológico.

Los índices se declaran en api-chatty (`Database/indexes`), como el resto.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, Iterable, List, Optional, Sequence

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from ....models.chat.chat_messages_bucket import (
    BUCKET_SIZE, ChatMessagesBucket, counts_as_visible, message_to_document,
)
from ....models.chat.message_summary import _as_utc
from ....models.messages.chatty_messages import ChattyMessage
from ....models.messages.meta_message_model.meta_status_json import ErrorDetail
from ....models.messages.meta_message_model.schema.values.motivos_de_no_entrega import NoEntrega
from ....models.utils import MessageType, Status
from ....models.utils.types.message_types import MessageSubtype
from ....models.utils.types.identifier import StrObjectId

# Los estados que un «leído hasta acá» puede avanzar a `read`: no prueba nada de un `failed` ni de un `waiting`.
READ_UP_TO_ADVANCES = (Status.SENT, Status.DELIVERED)

logger = logging.getLogger("ChatMessagesCollection")

COLLECTION_NAME = "chat_messages"
#: Reintentos cuando otro escritor gana la carrera por el último bloque.
MAX_WRITE_ATTEMPTS = 3


class AppendOutcome(StrEnum):
    APPENDED = "appended"
    DUPLICATE = "duplicate"


class BucketWriteConflict(Exception):
    """Otro escritor ganó la carrera por el último bloque más veces que los reintentos."""


@dataclass(frozen=True)
class MessagesWindow:
    """Los mensajes de los últimos bloques y cuántos visibles tiene el chat en total."""
    messages: List[ChattyMessage]
    total_visible: int


class ChatMessagesCollection:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    @classmethod
    def from_connection(cls, connection: Any, database: str) -> "ChatMessagesCollection":
        return cls(connection.client[database][COLLECTION_NAME])

    # ── Escritura de mensajes nuevos ──

    async def append(self, company_id: StrObjectId, chat_id: StrObjectId, message: ChattyMessage) -> AppendOutcome:
        """Agrega un mensaje al final del chat. Idempotente por id de mensaje."""
        for _ in range(MAX_WRITE_ATTEMPTS):
            last = await self.collection.find_one(
                {"chat_id": chat_id}, projection={"seq": 1, "count": 1}, sort=[("seq", -1)],
            )
            if last is not None and last["count"] < BUCKET_SIZE:
                outcome = await self._push_into(last["_id"], chat_id, message)
                if outcome is not None:
                    return outcome
                continue
            if await self.contains(chat_id, message.id):
                return AppendOutcome.DUPLICATE
            outcome = await self._open_bucket(company_id, chat_id, (last["seq"] if last else 0) + 1, [message])
            if outcome is not None:
                return outcome
        raise BucketWriteConflict(f"chat {chat_id}: no se pudo escribir el mensaje {message.id} tras {MAX_WRITE_ATTEMPTS} intentos")

    async def append_many(self, company_id: StrObjectId, chat_id: StrObjectId, messages: Iterable[ChattyMessage]) -> List[AppendOutcome]:
        """Varios mensajes nuevos en orden (el vuelco de `Chat.pending_messages`)."""
        return [await self.append(company_id, chat_id, m) for m in sorted(messages, key=lambda m: _as_utc(m.created_at))]

    async def _push_into(self, bucket_id: Any, chat_id: StrObjectId, message: ChattyMessage) -> Optional[AppendOutcome]:
        """El `$push` condicional al bloque. None = el bloque se llenó entre medio: reintentar."""
        created_at = _as_utc(message.created_at)
        try:
            result = await self.collection.update_one(
                {"_id": bucket_id, "count": {"$lt": BUCKET_SIZE}, "messages.id": {"$ne": message.id}},
                {
                    "$push": {"messages": message_to_document(message)},
                    "$inc": {"count": 1, "visible_count": 1 if counts_as_visible(message) else 0},
                    "$max": {"last_at": created_at},
                    "$min": {"first_at": created_at},
                },
            )
        except DuplicateKeyError:
            return AppendOutcome.DUPLICATE
        if result.modified_count:
            return AppendOutcome.APPENDED
        if await self.contains(chat_id, message.id):
            return AppendOutcome.DUPLICATE
        return None

    async def _open_bucket(self, company_id: StrObjectId, chat_id: StrObjectId, seq: int, messages: List[ChattyMessage]) -> Optional[AppendOutcome]:
        """Crea un bloque. None = otro escritor creó ese `seq` primero: reintentar."""
        try:
            await self.collection.insert_one(ChatMessagesBucket.new(company_id, chat_id, seq, messages).to_document())
            return AppendOutcome.APPENDED
        except DuplicateKeyError:
            if len(messages) == 1 and await self.contains(chat_id, messages[0].id):
                return AppendOutcome.DUPLICATE
            return None

    # ── Historial con fechas viejas (coexistence) ──

    async def insert_history(self, company_id: StrObjectId, chat_id: StrObjectId, messages: Sequence[ChattyMessage]) -> List[ChattyMessage]:
        """Inserta mensajes que pueden ser más viejos que los que ya tiene el chat.

        Devuelve los que ESTE llamador insertó (sin los que ya estaban ni los que otro escritor
        metió a la vez): el import emite eventos y mueve el resumen sólo sobre eso. Lo anterior
        al primer bloque va a bloques nuevos con `seq` negativo; lo que cae dentro del rango de
        un bloque existente se intercala en ese bloque, ordenado; lo posterior al último bloque
        sigue el camino de `append`.

        Sin lock por chat: dos escritores (un lease perdido, el mismo cliente por teléfono y por
        BSUID, el webhook en vivo) pueden chocar contra `{chat_id, seq}` o `{chat_id, messages.id}`.
        Ante un choque se relee qué falta y se reintenta, sin perder lo ya insertado.
        """
        unique: Dict[str, ChattyMessage] = {}
        for message in messages:
            unique.setdefault(message.id, message)
        inserted: List[ChattyMessage] = []
        for attempt in range(1, MAX_WRITE_ATTEMPTS + 1):
            try:
                await self._insert_history_once(company_id, chat_id, list(unique.values()), inserted)
                return sorted(inserted, key=lambda m: _as_utc(m.created_at))
            except DuplicateKeyError:
                if attempt == MAX_WRITE_ATTEMPTS:
                    raise BucketWriteConflict(f"historial de {chat_id}: otro escritor ganó {MAX_WRITE_ATTEMPTS} veces")
                logger.warning("historial de %s: choque con otro escritor; se relee lo que falta (intento %d)", chat_id, attempt)
        return sorted(inserted, key=lambda m: _as_utc(m.created_at))

    async def _insert_history_once(self, company_id: StrObjectId, chat_id: StrObjectId, messages: List[ChattyMessage], inserted: List[ChattyMessage]) -> None:
        """Una pasada: lo que todavía no está en el chat. Va anotando en `inserted` a medida que
        escribe, así un choque a mitad de pasada no pierde lo que ya entró."""
        existing = set(await self.existing_ids(chat_id, [m.id for m in messages]))
        new = sorted((m for m in messages if m.id not in existing), key=lambda m: _as_utc(m.created_at))
        if not new:
            return
        first = await self.collection.find_one({"chat_id": chat_id}, projection={"seq": 1, "first_at": 1}, sort=[("seq", 1)])
        if first is None:
            await self._insert_chunks(company_id, chat_id, new, start_seq=1, step=1, inserted=inserted)
            return
        first_at = _as_utc(first["first_at"])
        older = [m for m in new if _as_utc(m.created_at) < first_at]
        rest = [m for m in new if _as_utc(m.created_at) >= first_at]
        if older:
            await self._insert_chunks(company_id, chat_id, list(reversed(older)), start_seq=first["seq"] - 1, step=-1, inserted=inserted)
        for message in rest:
            if await self._insert_in_place(company_id, chat_id, message):
                inserted.append(message)

    async def _insert_chunks(self, company_id: StrObjectId, chat_id: StrObjectId, messages: List[ChattyMessage], start_seq: int, step: int, inserted: List[ChattyMessage]) -> None:
        """Bloques de hasta 50 desde `start_seq`, avanzando de a `step` (+1 hacia adelante, -1 hacia atrás)."""
        seq = start_seq
        for index in range(0, len(messages), BUCKET_SIZE):
            chunk = messages[index:index + BUCKET_SIZE]
            await self.collection.insert_one(ChatMessagesBucket.new(company_id, chat_id, seq, chunk).to_document())
            inserted.extend(chunk)
            seq += step

    async def _insert_in_place(self, company_id: StrObjectId, chat_id: StrObjectId, message: ChattyMessage) -> bool:
        """Intercala un mensaje en el bloque de su fecha. Devuelve si lo insertó este llamador."""
        created_at = _as_utc(message.created_at)
        bucket = await self.collection.find_one(
            {"chat_id": chat_id, "first_at": {"$lte": created_at}}, projection={"seq": 1, "last_at": 1}, sort=[("seq", -1)],
        )
        last = await self.collection.find_one({"chat_id": chat_id}, projection={"seq": 1}, sort=[("seq", -1)])
        if bucket is None or (last is not None and bucket["seq"] == last["seq"] and created_at >= _as_utc(bucket["last_at"])):
            return await self.append(company_id, chat_id, message) == AppendOutcome.APPENDED
        try:
            result = await self.collection.update_one(
                {"_id": bucket["_id"], "messages.id": {"$ne": message.id}},
                {
                    "$push": {"messages": {"$each": [message_to_document(message)], "$sort": {"created_at": 1}}},
                    "$inc": {"count": 1, "visible_count": 1 if counts_as_visible(message) else 0},
                    "$max": {"last_at": created_at},
                },
            )
        except DuplicateKeyError:
            logger.info("historial: %s ya estaba en otro bloque de %s", message.id, chat_id)
            return False
        return result.modified_count > 0

    # ── Lectura ──

    async def contains(self, chat_id: StrObjectId, message_id: str) -> bool:
        return await self.collection.find_one({"chat_id": chat_id, "messages.id": message_id}, projection={"_id": 1}) is not None

    async def existing_ids(self, chat_id: StrObjectId, message_ids: List[str]) -> List[str]:
        """De estos ids, los que el chat ya tiene."""
        if not message_ids:
            return []
        wanted = set(message_ids)
        stored = await self.collection.distinct("messages.id", {"chat_id": chat_id, "messages.id": {"$in": message_ids}})
        return [message_id for message_id in stored if message_id in wanted]

    async def last_window(self, chat_id: StrObjectId, visible: int) -> MessagesWindow:
        """Los últimos bloques hasta juntar `visible` mensajes visibles, en orden cronológico.

        Trae bloques enteros: las reacciones y los mensajes citados que caen en esos bloques
        vienen con ellos. `total_visible` es del chat entero, para `messages_pagination`.
        """
        headers = await self.collection.find({"chat_id": chat_id}, projection={"seq": 1, "visible_count": 1}).sort("seq", -1).to_list(None)
        total_visible = sum(h["visible_count"] for h in headers)
        wanted, gathered = [], 0
        for header in headers:
            wanted.append(header["_id"])
            gathered += header["visible_count"]
            if gathered >= visible:
                break
        if not wanted:
            return MessagesWindow(messages=[], total_visible=0)
        buckets = await self.collection.find({"_id": {"$in": wanted}}).to_list(None)
        return MessagesWindow(messages=self._messages_of(buckets), total_visible=total_visible)

    async def all_messages(self, chat_id: StrObjectId) -> List[ChattyMessage]:
        """Todo el historial del chat. Para las consultas que lo necesitan de verdad (un chat
        tiene 1 bloque en la mediana y 17 en el máximo medido)."""
        return self._messages_of(await self.collection.find({"chat_id": chat_id}).to_list(None))

    async def messages_by_ids(self, chat_id: StrObjectId, message_ids: List[str]) -> List[ChattyMessage]:
        """Mensajes puntuales (citados, reaccionados) que pueden estar fuera de la ventana."""
        if not message_ids:
            return []
        wanted = set(message_ids)
        buckets = await self.collection.find({"chat_id": chat_id, "messages.id": {"$in": message_ids}}).to_list(None)
        return [m for m in self._messages_of(buckets) if m.id in wanted]

    async def find_message(self, chat_id: StrObjectId, message_id: str) -> Optional[ChattyMessage]:
        found = await self.messages_by_ids(chat_id, [message_id])
        return found[0] if found else None

    async def central_notices_about(self, chat_id: StrObjectId, message_id: str) -> List[ChattyMessage]:
        """Las notificaciones centrales que apuntan a un mensaje (`context.message_id`). Acotado a
        `type: central`: nunca devuelve un mensaje del cliente."""
        match = {"type": MessageType.CENTRAL.value, "context.message_id": message_id}
        buckets = await self.collection.find({"chat_id": chat_id, "messages": {"$elemMatch": match}}).to_list(None)
        return [
            m for m in self._messages_of(buckets)
            if m.type == MessageType.CENTRAL and m.context is not None and m.context.message_id == message_id
        ]

    async def sent_fast_answer_ids(self, chat_id: StrObjectId) -> List[str]:
        """Las respuestas rápidas que ya salieron en el chat (su `context.response_id`), en todo
        el historial. Es lo que leía `Chat.sent_fast_answers_ids` recorriendo los mensajes."""
        return await self._context_values(chat_id, MessageSubtype.CHATTY_FAST_ANSWER, "response_id")

    async def sent_template_names(self, chat_id: StrObjectId) -> List[str]:
        """Los nombres de las plantillas que ya salieron en el chat, en todo el historial."""
        return await self._context_values(chat_id, MessageSubtype.TEMPLATE, "template_name")

    async def _context_values(self, chat_id: StrObjectId, subtype: MessageSubtype, field: str) -> List[str]:
        """Un campo de `context` de los mensajes de un subtipo, sin traer los bloques enteros."""
        pipeline = [
            {"$match": {"chat_id": chat_id, "messages.subtype": subtype.value}},
            {"$unwind": "$messages"},
            {"$match": {"messages.subtype": subtype.value}},
            {"$project": {"_id": 0, "value": f"$messages.context.{field}"}},
        ]
        rows = await self.collection.aggregate(pipeline).to_list(None)
        return [row["value"] for row in rows if row.get("value")]

    async def count_visible(self, chat_id: StrObjectId) -> int:
        """Mensajes visibles del chat entero, sumados de las cabeceras de sus bloques."""
        headers = await self.collection.find({"chat_id": chat_id}, projection={"visible_count": 1}).to_list(None)
        return sum(h["visible_count"] for h in headers)

    async def starred_messages(self, chat_id: StrObjectId) -> List[ChattyMessage]:
        buckets = await self.collection.find({"chat_id": chat_id, "messages.starred": True}).to_list(None)
        return [m for m in self._messages_of(buckets) if m.starred]

    @staticmethod
    def _messages_of(bucket_documents: List[Dict[str, Any]]) -> List[ChattyMessage]:
        messages: List[ChattyMessage] = []
        for document in sorted(bucket_documents, key=lambda d: d["seq"]):
            messages.extend(ChatMessagesBucket.from_document(document).messages)
        return sorted(messages, key=lambda m: _as_utc(m.created_at))

    # ── Cambios a un mensaje (posicionales, sin cargar el chat) ──

    async def update_status(self, chat_id: StrObjectId, message_id: str, status: Status, error_details: Optional[ErrorDetail] = None, *, confirmed_by_provider: bool) -> bool:
        """El ✓✓ del proveedor. Condicional: sólo entra si el estado guardado es uno que éste reemplaza
        (`Status.supersedes`), porque Meta manda sent/delivered/read sin orden garantizado."""
        superseded = [s.value for s in status.superseded_statuses(confirmed_by_provider=confirmed_by_provider)] + [None]
        fields: Dict[str, Any] = {"messages.$.status": status.value}
        if error_details:
            fields["messages.$.error_details"] = error_details.model_dump(mode="json")
            if status == Status.FAILED:
                fields["messages.$.no_entrega"] = NoEntrega.desde_error(
                    error_details.code, error_details.get_error_details() or error_details.message).model_dump(mode="json")
        result = await self.collection.update_one(
            {"chat_id": chat_id, "messages": {"$elemMatch": {"id": message_id, "status": {"$in": superseded}}}},
            {"$set": fields},
        )
        return result.matched_count > 0

    async def mark_read_up_to(self, chat_id: StrObjectId, up_to: datetime) -> List[str]:
        """Marca `read` los mensajes salientes del chat con fecha hasta `up_to` (inclusive). Devuelve los ids que
        ESTE llamador cambió.

        Es la lectura de los canales que avisan «leído hasta acá» en vez de un estado por mensaje. Sólo avanzan `sent`
        y `delivered`: un «leído hasta acá» no prueba nada de los anteriores, así que un `failed` o un `waiting` (un
        envío que no salió o no se confirmó) quedan como están. Cada mensaje entra por el mismo `update_status`
        condicional de siempre (`Status.supersedes`): uno que ya está `read`, o que otro escritor leyó a la vez, no se
        cuenta ni retrocede.
        """
        cutoff = _as_utc(up_to)
        buckets = await self.collection.find({"chat_id": chat_id, "first_at": {"$lte": cutoff}}).to_list(None)
        pending = [
            m for m in self._messages_of(buckets)
            if m.is_outgoing and _as_utc(m.created_at) <= cutoff and m.status in READ_UP_TO_ADVANCES
        ]
        marked: List[str] = []
        for message in pending:
            if await self.update_status(chat_id, message.id, Status.READ, confirmed_by_provider=True):
                marked.append(message.id)
        return marked

    async def set_message_fields(self, chat_id: StrObjectId, message_id: str, fields: Dict[str, Any]) -> bool:
        """`$set` posicional de campos del mensaje (`{"revoked": True}`, `{"content.body": ...}`)."""
        result = await self.collection.update_one(
            {"chat_id": chat_id, "messages.id": message_id},
            {"$set": {f"messages.$.{name}": value for name, value in fields.items()}},
        )
        return result.matched_count > 0

    async def pull(self, chat_id: StrObjectId, message_id: str) -> Optional[ChattyMessage]:
        """Saca un mensaje (el stub que reemplaza el mensaje real). Devuelve el que sacó."""
        message = await self.find_message(chat_id, message_id)
        if message is None:
            return None
        bucket = await self.collection.find_one_and_update(
            {"chat_id": chat_id, "messages.id": message_id},
            {"$pull": {"messages": {"id": message_id}}, "$inc": {"count": -1, "visible_count": -1 if counts_as_visible(message) else 0}},
            projection={"_id": 1},
        )
        if bucket is not None:
            # Un bloque vacío no se deja: dos bloques vacíos del mismo chat chocarían en el
            # índice único `{chat_id, messages.id}` (los dos indexan «sin id»).
            await self.collection.delete_one({"_id": bucket["_id"], "count": {"$lte": 0}})
        return message

    async def delete_chat(self, chat_id: StrObjectId) -> int:
        """Borra todos los bloques de un chat (borrado real del chat)."""
        result = await self.collection.delete_many({"chat_id": chat_id})
        return result.deleted_count
