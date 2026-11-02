"""`EntryRepository` on the `entradas` collection: a catalog read by id (`MongoCatalogById`) plus the fresh read and
the compare-and-set on `updated_at` of an edit that says which version it saw. Only Mongo: the cache is a decorator
(ADR-001)."""
from __future__ import annotations

from typing import Any, Optional, Tuple

from bson import ObjectId

from ...models.company.assets.atencion import Entrada
from ...models.utils.types import StrObjectId
from ...models.utils.types.serializer_type import SerializerType
from ..catalog_repository import MongoCatalogById


class MongoEntryRepository(MongoCatalogById[Entrada]):
    """Reuses the asset collection of the legacy `Entradas` service, so the stored document keeps its shape."""

    async def get_fresh(self, entry_id: StrObjectId) -> Entrada:
        return await self._read(entry_id)

    async def stored_updated_at(self, entry_id: StrObjectId) -> Tuple[bool, Any]:
        stored = await self.collection.collection.find_one({"_id": ObjectId(entry_id)}, projection={"updated_at": 1})
        return stored is not None, (stored or {}).get("updated_at")

    async def update_if_unchanged(self, current: Entrada, changes: Entrada, stored_updated_at: Any) -> Optional[Entrada]:
        # Only the fields `changes` brought (+ `updated_at`), as `update_fields`: one built without `account_ids` never
        # writes `[]` (= every account) nor overwrites what it did not send.
        updated, sent = current.merge(changes)
        updated.update_now()
        keys = {Entrada.model_fields[n].alias or n for n in sent if n in Entrada.model_fields} | {"updated_at"}
        document = {
            k: v for k, v in updated.model_dump_json(serializer=SerializerType.DATABASE).items()
            if k in keys and k != "_id"
        }
        result = await self.collection.collection.update_one(
            {"_id": ObjectId(current.id), "updated_at": stored_updated_at}, {"$set": document}
        )
        return updated if result.matched_count else None
