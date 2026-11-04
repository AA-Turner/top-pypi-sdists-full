"""`ChatFlowStateRepository` on `chat_flow_states`: the same queries `ChatFlowStateCollection.assign`, `remove`,
`update_fields`, `get` and `list_for_chat` ran, without touching `chats` (its `flow_ids` is api-chatty's
`ChatRepository`)."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional, Sequence

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from ...models.chat.flow_link_state import FlowStateAssignedToChat
from ...models.utils.custom_exceptions.custom_exceptions import AssetAlreadyAssigned

COLLECTION = "chat_flow_states"


class MongoChatFlowStateRepository:
    """On a Motor collection, handed in by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def insert(self, company_id: str, state: FlowStateAssignedToChat) -> None:
        if await self.collection.find_one({"chat_id": state.chat_id, "flow_id": state.flow_id}, projection={"_id": 1}):
            raise AssetAlreadyAssigned(f"Workflow {state.flow_id} ya asignado al chat {state.chat_id}", chat_id=state.chat_id)
        try:
            await self.collection.insert_one(state.to_document())
        except DuplicateKeyError:
            raise AssetAlreadyAssigned(f"Workflow {state.flow_id} ya asignado al chat {state.chat_id}", chat_id=state.chat_id)

    async def delete(self, company_id: str, chat_id: str, workflow_id: str) -> bool:
        result = await self.collection.delete_one({"chat_id": chat_id, "flow_id": workflow_id})
        return result.deleted_count > 0

    async def update(self, company_id: str, state_id: str, state: FlowStateAssignedToChat, fields: Sequence[str],
                     expected: Optional[Mapping[str, Optional[datetime]]] = None) -> bool:
        document = state.to_document()
        query: Dict[str, Any] = {"_id": ObjectId(state_id)}
        for name, value in (expected or {}).items():
            query[name] = value
        result = await self.collection.update_one(query, {"$set": {name: document[name] for name in fields}})
        return result.matched_count > 0

    async def get(self, company_id: str, state_id: str) -> Optional[FlowStateAssignedToChat]:
        document = await self.collection.find_one({"_id": ObjectId(state_id)})
        return FlowStateAssignedToChat.from_document(document) if document else None

    async def of_chat(self, company_id: str, chat_id: str) -> List[FlowStateAssignedToChat]:
        return FlowStateAssignedToChat.from_documents(await self.collection.find({"chat_id": chat_id}).to_list(None))
