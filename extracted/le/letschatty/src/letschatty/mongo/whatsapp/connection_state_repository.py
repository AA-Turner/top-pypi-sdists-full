"""`ConnectionStateRepository` on `whatsapp_connection_state`: the same filters and writes that api-chatty's
`company/whatsapp_connection/store.py` ran (a `find_one` by `_id`; version 0 is an `insert_one` and its
`DuplicateKeyError` means it lost; a later version is an `update_one` on `_id` and the version read; the banner `$set`
with `$inc` of the version; a conditional `delete_one`; the sweep's `status $ne connected`, of every company). No cache.

The stored shape is known only here: `_id` = the company for its default number and `company:account` for another
(`state_id_of`); `version` an integer beside the state's fields; the documents of before the accounts have neither
`company_id` nor `account_id` (they come from the `_id`)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from pymongo.errors import DuplicateKeyError

from ...domain.whatsapp.connection import ConnectionState, ConnectionStatus, state_id_of

COLLECTION = "whatsapp_connection_state"


class MongoConnectionStateRepository:
    """On a Motor collection, resolved by whoever wires it. The company is not in any filter, as before: the `_id`
    names the number."""

    def __init__(self, collection):
        self.collection = collection

    async def get(self, company_id: str, account_id: Optional[str]) -> Tuple[ConnectionState, int]:
        state_id = state_id_of(company_id, account_id)
        doc = await self.collection.find_one({"_id": state_id})
        if not doc:
            return ConnectionState.connected_for(state_id), 0
        version = int(doc.pop("version", 0))
        return state_from_document(doc), version

    async def compare_and_set(self, company_id: str, expected_version: int, state: ConnectionState) -> bool:
        body = state.model_dump(mode="python")
        body["version"] = expected_version + 1
        if expected_version == 0:
            try:
                await self.collection.insert_one({"_id": state.state_id, **body})
                return True
            except DuplicateKeyError:
                return False
        result = await self.collection.update_one({"_id": state.state_id, "version": expected_version}, {"$set": body})
        return result.modified_count == 1

    async def set_banner(self, company_id: str, account_id: Optional[str], notification_id: Optional[str],
                         expected_version: int) -> bool:
        result = await self.collection.update_one(
            {"_id": state_id_of(company_id, account_id), "version": expected_version},
            {"$set": {"banner_notification_id": notification_id}, "$inc": {"version": 1}},
        )
        return result.modified_count == 1

    async def delete(self, company_id: str, account_id: Optional[str], expected_version: int) -> bool:
        result = await self.collection.delete_one({"_id": state_id_of(company_id, account_id),
                                                   "version": expected_version})
        return result.deleted_count == 1

    async def not_connected(self) -> List[ConnectionState]:
        states = []
        async for doc in self.collection.find({"status": {"$ne": ConnectionStatus.CONNECTED.value}}):
            doc.pop("version", None)
            states.append(state_from_document(doc))
        return states


def state_from_document(doc: Dict[str, Any]) -> ConnectionState:
    """A document of `whatsapp_connection_state` (without its `version`). Those of before the accounts did not store
    `company_id` nor `account_id`: they are the company's default number (`_id = company_id`)."""
    fallback = ConnectionState.connected_for(str(doc.pop("_id")))
    doc.setdefault("company_id", fallback.company_id)
    doc.setdefault("account_id", fallback.account_id)
    return ConnectionState.model_validate(doc)
