"""`CoexistenceImportSyncRepository` on the `coexistence_import_sync` collection. Not a catalog (ADR-010 of api-chatty):
every write is the same atomic Mongo operation the asset service `CoexistenceImportSyncs` ran, with the same filters and
in the same order, because chunks of one import arrive concurrently and are redelivered. Only Mongo: the cache is a
decorator (ADR-001)."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pymongo import ReturnDocument

from ...models.chat.coexistence_import_sync import CoexistenceImportSync, ImportSyncStatus
from ...models.utils.types import StrObjectId


class MongoCoexistenceImportSyncRepository:
    """Reuses the asset collection of the legacy service, so the stored document keeps its shape (`insert` and
    `get_by_id` are the collection's own)."""

    def __init__(self, collection):
        self.collection = collection

    @property
    def _rows(self):
        return self.collection.collection

    async def of_company(self, company_id: StrObjectId) -> List[CoexistenceImportSync]:
        return await self.collection.get_docs(query={}, company_id=company_id)

    async def of_number(self, company_id: StrObjectId, phone_number_id: Optional[str]) -> List[CoexistenceImportSync]:
        return await self.collection.get_docs(query={"phone_number_id": phone_number_id}, company_id=company_id)

    async def adopt(self, sync_id: StrObjectId, phone_number_id: str) -> bool:
        result = await self._rows.update_one(
            {"_id": ObjectId(sync_id), "phone_number_id": None}, {"$set": {"phone_number_id": phone_number_id}},
        )
        return bool(result.modified_count)

    async def add(self, item: CoexistenceImportSync) -> None:
        await self.collection.insert(item)

    async def get(self, sync_id: StrObjectId) -> CoexistenceImportSync:
        return await self.collection.get_by_id(sync_id)

    async def apply_chunk(self, sync_id: StrObjectId, *, key: str, messages_delta: int, threads_delta: int,
                          contacts_delta: int, progress: Optional[float]) -> None:
        """Two atomic writes, never a read-then-write: the counters gated on the chunk key (`$ne` + `$addToSet`, so a
        redelivered chunk matches nothing), then contacts (FIX F: already counted once per waid upstream) and `$max`
        progress outside the gate, skipped when there is nothing to add."""
        oid = ObjectId(sync_id)
        await self._rows.update_one(
            {"_id": oid, "seen_chunks": {"$ne": key}},
            {
                "$addToSet": {"seen_chunks": key},
                "$inc": {"messages_imported": messages_delta, "threads_imported": threads_delta},
                "$currentDate": {"updated_at": True},
            },
        )
        accumulate: dict = {}
        if contacts_delta:
            accumulate["$inc"] = {"contacts_imported": contacts_delta}
        if progress is not None:
            accumulate["$max"] = {"max_progress": progress}
        if accumulate:
            accumulate["$currentDate"] = {"updated_at": True}
            await self._rows.update_one({"_id": oid}, accumulate)

    async def add_imported(self, sync_id: StrObjectId, *, messages_delta: int, threads_delta: int) -> None:
        await self._rows.update_one(
            {"_id": ObjectId(sync_id)},
            {
                "$inc": {"messages_imported": messages_delta, "threads_imported": threads_delta},
                "$currentDate": {"updated_at": True},
            },
        )

    async def touch_last_chunk(self, sync_id: StrObjectId, when: datetime) -> None:
        await self._rows.update_one({"_id": ObjectId(sync_id)}, {"$set": {"last_chunk_at": when}})

    async def reopen_if_completed(self, sync_id: StrObjectId) -> Optional[CoexistenceImportSync]:
        doc = await self._rows.find_one_and_update(
            {"_id": ObjectId(sync_id), "status": ImportSyncStatus.COMPLETED.value},
            {"$set": {"status": ImportSyncStatus.IN_PROGRESS.value}},
            return_document=ReturnDocument.AFTER,
        )
        return self.collection.create_instance(doc) if doc is not None else None

    async def complete_if_pending(self, sync_id: StrObjectId) -> Optional[CoexistenceImportSync]:
        doc = await self._rows.find_one_and_update(
            {"_id": ObjectId(sync_id), "status": {"$ne": ImportSyncStatus.COMPLETED.value}},
            {
                "$set": {"status": ImportSyncStatus.COMPLETED.value},
                "$currentDate": {"updated_at": True},
            },
            return_document=ReturnDocument.AFTER,
        )
        return self.collection.create_instance(doc) if doc is not None else None

    async def stale_in_progress(self, older_than: datetime) -> List[CoexistenceImportSync]:
        cursor = self._rows.find(
            {
                "status": ImportSyncStatus.IN_PROGRESS.value,
                "last_chunk_at": {"$ne": None, "$lt": older_than},
            }
        )
        return [self.collection.create_instance(doc) async for doc in cursor]

    async def set_notification_id(self, sync_id: StrObjectId, notification_id: str) -> None:
        await self._rows.update_one({"_id": ObjectId(sync_id)}, {"$set": {"notification_id": notification_id}})
