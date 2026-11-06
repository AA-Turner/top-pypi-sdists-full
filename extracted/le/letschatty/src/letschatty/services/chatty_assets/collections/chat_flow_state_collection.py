"""Los estados de workflow de los chats: la colección `chat_flow_states`, un documento por estado.

Reemplaza a `chats.flow_states[]`, cuyos índices pesaban 806 MB (el 64% de los de `chats`) para
un campo presente en el 6,4% de los chats. Esta colección también mantiene `chats.flow_ids`, el
espejo que usa el filtro de workflows de la bandeja: se agrega al asignar y se saca al quitar.

`mark_chat_changed` es la marca de cambio que reemplazó a la comparación de `updated_at`:
despierta (`next_call = ahora`) sólo los estados que esperan un cambio del chat.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError
from zoneinfo import ZoneInfo

from ....models.chat.flow_link_state import FlowStateAssignedToChat, TRIGGERS_WOKEN_BY_CHAT_CHANGE
from ....models.utils.custom_exceptions.custom_exceptions import AssetAlreadyAssigned
from ....models.utils.types.identifier import StrObjectId

COLLECTION_NAME = "chat_flow_states"
_MARK_BATCH = 500


def _now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))


class ChatFlowStateCollection:
    def __init__(self, collection: AsyncIOMotorCollection, chats: AsyncIOMotorCollection):
        self.collection = collection
        self.chats = chats

    @classmethod
    def from_connection(cls, connection: Any, database: str) -> "ChatFlowStateCollection":
        db = connection.client[database]
        return cls(db[COLLECTION_NAME], db["chats"])

    async def list_for_chat(self, chat_id: StrObjectId, now: Optional[datetime] = None) -> List[FlowStateAssignedToChat]:
        documents = await self.collection.find({"chat_id": chat_id}).to_list(None)
        return FlowStateAssignedToChat.from_documents(documents, now=now)

    async def list_for_chats(self, chat_ids: List[StrObjectId]) -> Dict[StrObjectId, List[FlowStateAssignedToChat]]:
        by_chat: Dict[StrObjectId, List[FlowStateAssignedToChat]] = {chat_id: [] for chat_id in chat_ids}
        for state in FlowStateAssignedToChat.from_documents(await self.collection.find({"chat_id": {"$in": chat_ids}}).to_list(None)):
            by_chat.setdefault(state.chat_id, []).append(state)
        return by_chat

    async def get(self, state_id: StrObjectId) -> Optional[FlowStateAssignedToChat]:
        document = await self.collection.find_one({"_id": ObjectId(state_id)})
        return FlowStateAssignedToChat.from_document(document) if document else None

    async def assign(self, state: FlowStateAssignedToChat) -> FlowStateAssignedToChat:
        """Asigna un workflow a un chat. Uno por workflow y chat (único `{chat_id, flow_id}`)."""
        if await self.collection.find_one({"chat_id": state.chat_id, "flow_id": state.flow_id}, projection={"_id": 1}):
            raise AssetAlreadyAssigned(f"Workflow {state.flow_id} ya asignado al chat {state.chat_id}", chat_id=state.chat_id)
        try:
            await self.collection.insert_one(state.to_document())
        except DuplicateKeyError:
            raise AssetAlreadyAssigned(f"Workflow {state.flow_id} ya asignado al chat {state.chat_id}", chat_id=state.chat_id)
        await self.chats.update_one({"_id": ObjectId(state.chat_id)}, {"$addToSet": {"flow_ids": state.flow_id}})
        return state

    async def remove(self, chat_id: StrObjectId, flow_id: StrObjectId) -> bool:
        """Quita el workflow del chat: borra el estado y lo saca de `flow_ids`."""
        result = await self.collection.delete_one({"chat_id": chat_id, "flow_id": flow_id})
        await self.chats.update_one({"_id": ObjectId(chat_id)}, {"$pull": {"flow_ids": flow_id}})
        return result.deleted_count > 0

    async def update_fields(self, state_id: StrObjectId, fields: Dict[str, Any], expected: Optional[Dict[str, Any]] = None) -> bool:
        """`$set` de los campos que cambiaron, nunca del estado entero.

        Con `expected`, es compare-and-set: sólo escribe si esos campos siguen valiendo lo que
        valían cuando se leyó el estado. copilot pasa `{"last_call": ..., "next_call": ...}`: si
        la marca de cambio movió `next_call` entre su lectura y su escritura, la escritura no
        entra y el estado se reevalúa en el próximo tick, en vez de borrar el despertar.
        Devuelve si escribió.
        """
        query: Dict[str, Any] = {"_id": ObjectId(state_id)}
        for name, value in (expected or {}).items():
            query[name] = value
        fields = dict(fields)
        fields.pop("_id", None)
        fields.pop("id", None)
        if "asset_id" in fields:
            fields["flow_id"] = fields.pop("asset_id")
        result = await self.collection.update_one(query, {"$set": fields})
        return result.matched_count > 0

    async def mark_chat_changed(self, chat_id: StrObjectId, now: Optional[datetime] = None) -> int:
        """Algo que una condición puede leer cambió en el chat: despierta los estados que esperan
        un cambio. Los de trigger `next_call` no se tocan. Devuelve cuántos despertó."""
        result = await self.collection.update_many(
            {"chat_id": chat_id, "trigger": {"$in": list(TRIGGERS_WOKEN_BY_CHAT_CHANGE)}},
            {"$set": {"next_call": now or _now()}},
        )
        return result.modified_count

    async def mark_chats_changed(self, chat_ids: List[StrObjectId], now: Optional[datetime] = None) -> int:
        """`mark_chat_changed` para muchos chats a la vez (las escrituras en lote de `chats`:
        liberar o archivar los chats de un agente, soltar un funnel). De a tandas."""
        woken, now = 0, now or _now()
        for start in range(0, len(chat_ids), _MARK_BATCH):
            result = await self.collection.update_many(
                {"chat_id": {"$in": list(chat_ids[start:start + _MARK_BATCH])}, "trigger": {"$in": list(TRIGGERS_WOKEN_BY_CHAT_CHANGE)}},
                {"$set": {"next_call": now}},
            )
            woken += result.modified_count
        return woken
