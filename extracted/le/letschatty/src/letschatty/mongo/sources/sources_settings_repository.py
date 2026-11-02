"""`SourcesSettingsRepository` on the `sources_settings` collection: the same two Mongo operations the legacy service
of api-chatty ran (`find_one` with a projection, `update_one` with `$set` and upsert), keyed by the company id as
text."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

_NOT_SETTINGS = {"_id": 0, "updated_by": 0, "updated_at": 0}


class MongoSourcesSettingsRepository:
    """On a Motor collection, resolved by whoever wires it (api-chatty resolves it on every call)."""

    def __init__(self, collection):
        self.collection = collection

    async def stored(self, company_id: str) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one({"_id": str(company_id)}, projection=_NOT_SETTINGS)

    async def save(self, company_id: str, settings: Dict[str, Any], *, updated_by: Optional[str],
                   updated_at: datetime) -> None:
        await self.collection.update_one(
            {"_id": str(company_id)},
            {"$set": {**settings, "updated_by": updated_by, "updated_at": updated_at}},
            upsert=True,
        )
