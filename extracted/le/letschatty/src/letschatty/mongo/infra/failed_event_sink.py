"""`FailedEventSink` on the `failed_events` collection: the one Mongo operation the legacy service of api-chatty ran
(`insert_many`, ordered, the records handed in)."""
from __future__ import annotations

from typing import Any, Dict, List


class MongoFailedEventSink:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def insert_many(self, records: List[Dict[str, Any]]) -> List[Any]:
        result = await self.collection.insert_many(records)
        return result.inserted_ids
