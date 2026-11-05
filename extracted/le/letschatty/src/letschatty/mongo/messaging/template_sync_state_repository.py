"""`TemplateSyncStateRepository` on the `template_sync_state` collection: the same Mongo operations the legacy store
of api-chatty ran (`find_one` by the key, `update_one` with `$set` and upsert), with the key `waba_id` + `company_id`
as text. Prod has no unique index on the key (only `_id`)."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from ...domain.messaging.template_sync_state import TemplateSyncState

READ_ORDER = "_mongo_read_order"
STORED_ID = "_mongo_stored_id"
# The stored names the model names; any other key goes to `others`, as stored.
KNOWN = ("_id", "company_id", "waba_id", "last_synced_at", "last_sync_error", "message_template_limit",
         "updated_at")


def _key(company_id: str, waba_id: str) -> dict:
    return {"waba_id": waba_id, "company_id": company_id}


class MongoTemplateSyncStateRepository:
    """On a Motor collection, resolved by whoever wires it (api-chatty resolves it on every call)."""

    def __init__(self, collection):
        self.collection = collection

    async def get(self, company_id: str, waba_id: str) -> Optional[TemplateSyncState]:
        doc = await self.collection.find_one(_key(company_id, waba_id))
        if doc is None:
            return None
        state = TemplateSyncState(
            id=str(doc["_id"]), company_id=doc.get("company_id"), waba_id=doc.get("waba_id"),
            last_synced_at=doc.get("last_synced_at"), last_sync_error=doc.get("last_sync_error"),
            message_template_limit=doc.get("message_template_limit"), updated_at=doc.get("updated_at"),
            others={key: value for key, value in doc.items() if key not in KNOWN})
        # The keys of the document, in the order Mongo gave them, and the `_id` as stored: storage details, so they are
        # not fields of the model (what the legacy store hands its callers is the document as `main` did).
        object.__setattr__(state, READ_ORDER, tuple(doc))
        object.__setattr__(state, STORED_ID, doc["_id"])
        return state

    async def mark_synced(self, company_id: str, waba_id: str, *, at: datetime,
                          message_template_limit: Optional[int]) -> None:
        await self.collection.update_one(
            _key(company_id, waba_id),
            {"$set": {"last_synced_at": at, "last_sync_error": None, "message_template_limit": message_template_limit,
                      "updated_at": at}},
            upsert=True,
        )

    async def mark_error(self, company_id: str, waba_id: str, *, error: str, at: datetime) -> None:
        await self.collection.update_one(
            _key(company_id, waba_id),
            {"$set": {"last_sync_error": error, "updated_at": at}},
            upsert=True,
        )
