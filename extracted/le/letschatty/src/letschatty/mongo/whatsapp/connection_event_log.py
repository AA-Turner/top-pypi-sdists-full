"""`ConnectionEventLog` on `whatsapp_connection_events`: the same operations that api-chatty's
`company/whatsapp_connection/store.py` ran (an `insert_one` whose `DuplicateKeyError` means «already there», a
`delete_one` and an `update_one` `$set` by `_id`, a `find_one` by company, source and `occurred_at`, and the company's
newest entries without `raw`). No cache. The TTL index on `occurred_at` deletes the entries (api-chatty
`Database/indexes/whatsapp_connection_events_indexes.py`).

The stored shape: `_id` = the event's `id`, then the fields the event was given, in the model's order (`main`'s), the
explicit nulls included; a field that was not given is not stored. The company is not in the filters by key, as
before: the key names the entry."""
from __future__ import annotations

from datetime import datetime
from typing import List

from pymongo.errors import DuplicateKeyError

from ...domain.whatsapp.connection import ConnectionEvent
from ...domain.whatsapp.connection_store import ConnectionEventOutcome

COLLECTION = "whatsapp_connection_events"


class MongoConnectionEventLog:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def claim(self, company_id: str, event: ConnectionEvent) -> bool:
        try:
            await self.collection.insert_one({"_id": event.id, **event.model_dump(exclude_unset=True, exclude={"id"}, warnings=False)})
            return True
        except DuplicateKeyError:
            return False

    async def release(self, company_id: str, event_id: str) -> None:
        await self.collection.delete_one({"_id": event_id})

    async def record_outcome(self, company_id: str, event_id: str, outcome: ConnectionEventOutcome) -> None:
        await self.collection.update_one({"_id": event_id}, {"$set": outcome.model_dump(exclude_unset=True, warnings=False)})

    async def has_event_since(self, company_id: str, source: str, since: datetime) -> bool:
        doc = await self.collection.find_one(
            {"company_id": company_id, "source": source, "occurred_at": {"$gte": since}}, {"_id": 1})
        return doc is not None

    async def recent(self, company_id: str, limit: int) -> List[ConnectionEvent]:
        """Each entry as it is stored, without validating it (`main` handed the card the document): a stored value
        never makes the card fail."""
        cursor = self.collection.find({"company_id": company_id}, {"raw": 0}).sort("occurred_at", -1).limit(limit)
        return [ConnectionEvent.model_construct(id=doc.pop("_id"), **doc) async for doc in cursor]
