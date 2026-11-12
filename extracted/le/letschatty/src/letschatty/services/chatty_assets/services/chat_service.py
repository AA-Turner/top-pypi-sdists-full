"""Chat Service — la persistencia de un chat repartida en sus colecciones.

Un mensaje nuevo se escribe en este orden, sin transacción ni lock:

1. el bloque de `chat_messages` (idempotente por wamid);
2. el resumen en `chats`, con guarda «sólo si es más nuevo»;
3. si no es una nota del sistema (entrante o saliente), la marca de cambio de sus workflows:
   las condiciones de copilot leen el último entrante, el último saliente y su ✓✓.

Si el wamid ya estaba, se repiten 2 y 3 igual (la guarda los hace idempotentes): así una
re-entrega cura un resumen que no llegó a escribirse porque el pedido anterior falló entre el
bloque y el resumen. `rebuild_summary` lo rehace desde los bloques. Los cambios a un mensaje (✓✓, edición, revocación) tocan su bloque y, si es el último,
el resumen. Cualquier escritura de algo que una condición de workflow puede leer pasa por
`partial_update`, que pone la marca sola: ningún llamador se la puede olvidar.
"""

from typing import Iterable, List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import logging
import os

from pymongo.errors import DuplicateKeyError

from ..collections import ChatCollection
from ..collections.chat_messages_collection import AppendOutcome, ChatMessagesCollection
from ..collections.chat_flow_state_collection import ChatFlowStateCollection
from ..collections.client_collection import ClientCollection
from ....models.cache import CacheProtocol, NoCache, CacheConfig
from ....models.chat.chat import Chat
from ....models.chat.chat_summary import ChatSummary, counts_as_incoming_activity, opens_window
from ....models.data_base.mongo_connection import MongoConnection
from ....models.messages.chatty_messages import ChattyMessage
from ....models.utils import Status
from ....models.utils.types.message_types import MessageType
from ....models.utils.types.identifier import StrObjectId
from ....models.messages.meta_message_model.meta_status_json import ErrorDetail
from ....models.execution.execution import ExecutionContext
from ....models.utils.custom_exceptions.custom_exceptions import ChatAlreadyExists
from ....models.utils.types.deletion_type import DeletionType

logger = logging.getLogger("ChatAssetService")
# The cache read and invalidation helpers below were `ChattyAssetContainerWithCollection`'s: their ERROR lines keep its logger name
# (the «api-chatty · prod errores» alert and the Grafana queries look for it).
_container_logger = logging.getLogger("ChattyAssetContainerWithCollection")

#: Campos de `chats` que una condición de workflow puede leer. Escribir cualquiera despierta los
#: workflows del chat que esperan un cambio. Es una lista cerrada a propósito: lo que no está
#: (leído, destacado, borradores de la IA, el estado ✓✓) no dispara nada.
CONDITIONABLE_FIELDS = frozenset({
    "tags", "products", "sales", "contact_points", "active_funnel", "lead_quality",
    "area", "agent_id", "chatty_ai_agent_in_chat_status",
})


def touches_conditionable_field(fields: Iterable[str]) -> bool:
    """Si alguna de estas rutas (`tags`, `active_funnel.stage_id`...) es de un campo condicionante."""
    return any(path.split(".", 1)[0] in CONDITIONABLE_FIELDS for path in fields)


def _history_candidates(messages: List[ChattyMessage]) -> List[ChattyMessage]:
    """De un lote de historial, los pocos mensajes que pueden mover el resumen.

    La guarda es monótona, así que aplicar sólo el último mensaje real, el último entrante, el
    último que abre ventana, el último entrante desde un anuncio, el último saliente y el primer
    saliente deja el mismo resumen que aplicar los miles del lote, con seis escrituras en vez de miles.
    """
    ordered = sorted(messages, key=lambda m: m.created_at)
    picks = []
    real = [m for m in ordered if m.type != MessageType.CENTRAL]
    incoming = [m for m in ordered if counts_as_incoming_activity(m)]
    windowed = [m for m in incoming if opens_window(m)]
    with_ad = [m for m in windowed if not m.referral.is_default]
    outgoing = [m for m in ordered if m.is_outgoing]
    for group in (real, incoming, windowed, with_ad, outgoing):
        if group:
            picks.append(group[-1])
    if outgoing:
        picks.append(outgoing[0])
    unique = {m.id: m for m in picks}
    return sorted(unique.values(), key=lambda m: m.created_at)


class ChatAssetService:
    """The Chat aggregate's store: composes `ChatCollection` (ENG-406: it no longer inherits `AssetService`).

    Only what the Chat aggregate uses stayed: `get_by_id`, `insert`, `partial_update`, `delete`, `get_by_query` and
    `collection`. The cache keys and their invalidation are the ones `AssetService` had, so the Redis calls do not change
    (`chats:item:{id}` is no longer written by `get_by_id` in api-chatty, but it is still deleted).

    Note: No event configuration - Chat events are handled by ChatsEditor, not AssetService.
    """

    def __init__(self,
                 connection: MongoConnection,
                 cache_config: CacheConfig = CacheConfig.default(),
                 cache: Optional[CacheProtocol] = None,
                 messages: Optional[ChatMessagesCollection] = None,
                 flow_states: Optional[ChatFlowStateCollection] = None,
                 clients: Optional[ClientCollection] = None):
        collection = ChatCollection(connection)
        self.item_type = collection.type
        self.preview_type = collection.preview_type
        self.collection = collection
        self.cache_config = cache_config or CacheConfig.default()
        self.cache: CacheProtocol = cache or NoCache()
        self._collection_name = collection.collection.name
        database = os.environ["MONGO_DB_NAME"]
        self.messages = messages or ChatMessagesCollection.from_connection(connection, database)
        self.flow_states = flow_states or ChatFlowStateCollection.from_connection(connection, database)
        self.clients = clients or ClientCollection(connection, chats=collection.collection)

    # ── Cache keys and what a write lets go of (the same ones `AssetService` used) ──

    def _item_key(self, item_id: str) -> str:
        return f"{self._collection_name}:item:{item_id}"

    def _previews_key(self, company_id: Optional[str]) -> str:
        return f"{self._collection_name}:previews:{company_id or 'all'}"

    def _all_key(self, company_id: Optional[str]) -> str:
        return f"{self._collection_name}:all:{company_id or 'all'}"

    def _list_keys(self, company_id: Optional[str]) -> list[str]:
        keys = [self._previews_key(company_id), self._all_key(company_id)]
        if company_id:
            keys += [self._previews_key(None), self._all_key(None)]
        return keys

    async def _invalidate(self, item: Chat) -> None:
        company_id = getattr(item, 'company_id', None)
        await self._delete_cache_keys([self._item_key(item.id), *self._list_keys(company_id)])

    async def _delete_cache_keys(self, keys: list[str]) -> None:
        """Invalidate `keys` after a write that MongoDB already accepted: a failed delete does not fail the write,
        it is logged at ERROR (the keys may serve the old value until their TTL)."""
        try:
            await self.cache.delete_many(keys)
        except Exception as e:
            _container_logger.error(
                "Redis cache invalidation failed after a saved write, keys may be stale until their TTL: %s (%s: %s)",
                keys, type(e).__name__, e,
            )

    async def _read_cache(self, key: str) -> Optional[str]:
        """Read `key` from the cache; a failed read is a miss (CHAT-277), logged at ERROR."""
        try:
            return await self.cache.get(key)
        except Exception as e:
            _container_logger.error(
                "Redis cache read failed, falling back to MongoDB: %s (%s: %s)",
                key, type(e).__name__, e,
            )
            return None

    # ── Base operations ──

    async def get_by_id(self, id: str, ignore_cache: bool = False) -> Chat:
        key = self._item_key(id)
        if not ignore_cache:
            cached = await self._read_cache(key)
            if cached:
                try:
                    return self.item_type.model_validate(json.loads(cached))
                except Exception:
                    pass
        item = await self.collection.get_by_id(id)
        try:
            await self.cache.set(key, json.dumps(item.model_dump(by_alias=True, mode='json')), ttl=self.cache_config.cache_ttl)
        except Exception:
            pass
        return item

    async def insert(self, item: Chat, execution_context: ExecutionContext) -> Chat:
        if not isinstance(item, self.item_type):
            raise TypeError(f"Expected item of type {self.item_type.__name__}, got {type(item).__name__}")
        await self.collection.insert(item)
        execution_context.set_event_time(item.created_at)
        await self._invalidate(item)
        return item

    async def delete(self, id: str, execution_context: ExecutionContext, deletion_type: DeletionType = DeletionType.LOGICAL) -> Chat:
        item = await self.get_by_id(id)
        await self.collection.delete(id, deletion_type)
        execution_context.set_event_time(datetime.now(ZoneInfo("UTC")))
        await self._invalidate(item)
        return item

    async def get_by_query(self, query: dict, company_id: Optional[StrObjectId] = None) -> List[Chat]:
        """Always hits MongoDB."""
        return await self.collection.get_docs(query=query, company_id=company_id)

    @property
    def _chat_collection(self) -> ChatCollection:
        return self.collection  # type: ignore[return-value]

    # ── Crear y guardar ──

    async def create(self, chat: Chat, execution_context: ExecutionContext) -> Chat:
        """Inserta el chat y escribe sus mensajes pendientes (el primero, si lo trae).

        Con la persona cargada (`ChatFactory.from_client`), primero la busca en `clients` por
        su identidad y, si no está, la da de alta: el chat queda apuntando a la persona que
        quedó guardada. Sin la persona cargada, `client_id` tiene que apuntar a una que exista.
        """
        if chat.person_loaded:
            chat.attach_person(await self.clients.find_or_insert(chat.person))
        try:
            await self.insert(chat, execution_context)
        except DuplicateKeyError as e:
            existing = await self._live_chat_of(chat) if "uniq_live_chat_per_account" in str(e) else None
            if existing is None:
                raise
            logger.warning("Chat for person %s in account %s of company %s already exists (%s): not creating another",
                           chat.client_id, chat.account_id, chat.company_id, existing)
            raise ChatAlreadyExists(chat_id=existing) from e
        await self.save_pending_messages(chat, execution_context)
        return chat

    async def _live_chat_of(self, chat: Chat) -> Optional[str]:
        """The id of the live chat that holds `chat`'s key in `uniq_live_chat_per_account`."""
        document = await self._chat_collection.collection.find_one(
            {"company_id": chat.company_id, "account_id": chat.account_id, "client_id": chat.client_id,
             "deleted_at": None, "legacy_duplicate_key": None},
            {"_id": 1},
        )
        return str(document["_id"]) if document else None

    async def save_pending(self, chat: Chat, execution_context: ExecutionContext) -> List[ChattyMessage]:
        """Guarda lo que la lógica en memoria dejó pendiente en el chat: los cambios de la persona
        (en `clients`, con fan-out a sus chats) y los mensajes nuevos. Devuelve los mensajes escritos."""
        await self.save_pending_person(chat)
        return await self.save_pending_messages(chat, execution_context)

    async def save_pending_person(self, chat: Chat) -> List[StrObjectId]:
        """Escribe los cambios de la persona y despierta los workflows de todos sus chats."""
        fields = chat.take_pending_person_fields()
        if not fields:
            return []
        touched = await self.clients.update_person(chat.client_id, fields)
        for chat_id in touched:
            await self.flow_states.mark_chat_changed(chat_id)
        return touched

    async def save_pending_messages(self, chat: Chat, execution_context: ExecutionContext) -> List[ChattyMessage]:
        """Escribe los mensajes que la lógica en memoria agregó al chat (`Chat.pending_messages`)."""
        written = []
        for message in chat.take_pending_messages():
            if await self.push_message(chat, message, execution_context) == AppendOutcome.APPENDED:
                written.append(message)
        return written

    async def push_message(self, chat: Chat, message: ChattyMessage, execution_context: ExecutionContext) -> AppendOutcome:
        """Escribe un mensaje nuevo: bloque, resumen y, si es del cliente, la marca de workflows.

        El `chat` en memoria queda igual que lo guardado (resumen al día, el mensaje fuera de
        los pendientes), para que lo que siga en el mismo pedido lea las ventanas correctas.
        `DUPLICATE` = ese wamid ya estaba: no se escribe nada más.
        """
        outcome = await self.messages.append(chat.company_id, chat.id, message)
        chat.mark_message_saved(message)
        if outcome == AppendOutcome.DUPLICATE:
            logger.info("[push_message] %s ya estaba en el chat %s: se reaplica el resumen", message.id, chat.id)
        chat.apply_summary(chat.summary.after(message))
        await self._chat_collection.apply_message(chat.id, message)
        if message.type != MessageType.CENTRAL:
            await self.flow_states.mark_chat_changed(chat.id)
        execution_context.set_event_time(message.created_at)
        await self.cache.delete(self._item_key(chat.id))
        return outcome

    async def insert_history(self, chat: Chat, messages: List[ChattyMessage], execution_context: ExecutionContext) -> List[ChattyMessage]:
        """Historial importado (coexistence): puede ser más viejo que lo que ya tiene el chat.
        Devuelve los mensajes que no estaban."""
        new = await self.messages.insert_history(chat.company_id, chat.id, messages)
        for message in _history_candidates(new):
            await self._chat_collection.apply_message(chat.id, message)
        await self.cache.delete(self._item_key(chat.id))
        return new

    async def partial_update(self, id: str, fields: dict, execution_context: ExecutionContext, invalidate_previews: bool = False, company_id: Optional[str] = None) -> None:
        """`$set` de campos del chat. Si alguno es condicionante, despierta sus workflows."""
        await self.collection.partial_update(id, fields)
        execution_context.set_event_time(datetime.now(ZoneInfo("UTC")))
        keys = [self._item_key(id)]
        if invalidate_previews and company_id:
            keys += self._list_keys(company_id)
        await self._delete_cache_keys(keys)
        if touches_conditionable_field(fields):
            await self.flow_states.mark_chat_changed(id)

    async def mark_chat_changed(self, chat_id: StrObjectId) -> None:
        """Para los cambios que no pasan por `partial_update` (la persona, en `clients`)."""
        await self.flow_states.mark_chat_changed(chat_id)

    async def mark_chats_changed(self, chat_ids: List[StrObjectId]) -> None:
        """Para las escrituras en lote de un campo condicionante (`update_many` sobre `chats`)."""
        if chat_ids:
            await self.flow_states.mark_chats_changed(chat_ids)

    # ── Cambios a un mensaje ──

    async def update_message_status(
        self,
        chat_id: str,
        message_id: str,
        status: Status,
        execution_context: ExecutionContext,
        error_details: Optional[ErrorDetail] = None,
        *,
        confirmed_by_provider: bool,
    ) -> bool:
        """El ✓✓: en el bloque y, si es el último mensaje, en el resumen. Devuelve si se aplicó
        (un estado que llega después de uno posterior se ignora, `Status.supersedes`)."""
        applied = await self.messages.update_status(chat_id, message_id, status, error_details, confirmed_by_provider=confirmed_by_provider)
        if applied:
            await self._chat_collection.apply_status(chat_id, message_id, status, error_details, confirmed_by_provider=confirmed_by_provider)
            if status == Status.READ:
                # «El cliente leyó» es una condición de copilot.
                await self.flow_states.mark_chat_changed(chat_id)
        await self.cache.delete(self._item_key(chat_id))
        return applied

    async def mark_read_up_to(self, chat_id: str, message_id: str, execution_context: ExecutionContext) -> List[str]:
        """«Leído hasta acá»: marca `read` los salientes del chat hasta la fecha del mensaje `message_id`
        (inclusive) que están en `sent` o `delivered` (un `failed` o un `waiting` quedan como están), en los bloques y en
        el resumen. Devuelve los ids que cambió; un mensaje que el chat no tiene
        no marca nada. Despierta los workflows si cambió alguno («el cliente leyó» es una condición de copilot)."""
        boundary = await self.messages.find_message(chat_id, message_id)
        marked = await self.messages.mark_read_up_to(chat_id, boundary.created_at) if boundary is not None else []
        for marked_id in marked:
            await self._chat_collection.apply_status(chat_id, marked_id, Status.READ, None, confirmed_by_provider=True)
        if marked:
            await self.flow_states.mark_chat_changed(chat_id)
        await self.cache.delete(self._item_key(chat_id))
        return marked

    async def update_message_revoked(self, chat_id: str, message_id: str, execution_context: ExecutionContext) -> None:
        """Marca el mensaje como borrado por quien lo mandó. El contenido se conserva."""
        if await self.messages.set_message_fields(chat_id, message_id, {"revoked": True}):
            await self._refresh_last_message(chat_id, message_id)
        await self.cache.delete(self._item_key(chat_id))

    async def update_message_edited(self, chat_id: str, message_id: str, new_body: str, edited_at: datetime, execution_context: ExecutionContext) -> None:
        """Aplica la edición del texto (y la leyenda «editado»), y la lleva al resumen si es el último."""
        if await self.messages.set_message_fields(chat_id, message_id, {"content.body": new_body, "context.edited_at": edited_at.isoformat(), "updated_at": edited_at.isoformat()}):
            await self._refresh_last_message(chat_id, message_id)
        await self.cache.delete(self._item_key(chat_id))

    async def update_message_played_at(self, chat_id: str, message_id: str, played_at: datetime, execution_context: ExecutionContext) -> None:
        """Cuándo se escuchó el audio. No toca el estado: no es un estado de entrega."""
        await self.messages.set_message_fields(chat_id, message_id, {"played_at": played_at.isoformat() if isinstance(played_at, datetime) else played_at})
        await self.cache.delete(self._item_key(chat_id))

    async def update_message_starred(self, chat_id: str, message_id: str, starred: bool, execution_context: ExecutionContext) -> None:
        await self.messages.set_message_fields(chat_id, message_id, {"starred": starred})
        await self.cache.delete(self._item_key(chat_id))

    async def remove_message(self, chat_id: str, message_id: str, execution_context: ExecutionContext) -> Optional[ChattyMessage]:
        """Saca un mensaje (el stub que reemplaza el mensaje real). Si era el último, rehace el resumen."""
        removed = await self.messages.pull(chat_id, message_id)
        if removed is not None:
            chat = await self.get_by_id(chat_id)
            if chat.last_message and chat.last_message.id == message_id:
                await self.rebuild_summary(chat_id)
        await self.cache.delete(self._item_key(chat_id))
        return removed

    async def rebuild_summary(self, chat_id: str) -> ChatSummary:
        """Rehace el resumen desde los bloques. Para reparar un resumen que quedó atrás."""
        summary = ChatSummary.from_messages(await self.messages.all_messages(chat_id))
        await self._chat_collection.write_summary(chat_id, summary)
        await self.cache.delete(self._item_key(chat_id))
        return summary

    async def _refresh_last_message(self, chat_id: str, message_id: str) -> None:
        message = await self.messages.find_message(chat_id, message_id)
        if message is not None:
            await self._chat_collection.refresh_last_message(chat_id, message)
