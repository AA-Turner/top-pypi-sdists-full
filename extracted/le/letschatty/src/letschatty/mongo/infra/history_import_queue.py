"""`HistoryImportQueue` and `ChatLeases` on Mongo: what `company/chats/coexistence/import_queue_mongo.py` of api-chatty
ran, moved as it was (the same filters, sorts, limits and atomic writes).

Two collections:

- `coexistence_import_jobs`: one document per thread. Indexes in api-chatty's
  `Database/indexes/coexistence_import_jobs_indexes.py` (the claim is an IXSCAN; `done` expires by itself after 7 days;
  `failed` never does, nor the old `overflow`).
- `coexistence_import_chat_leases`: the mutual exclusion per chat. The uniqueness of `_id` IS the lock: two workers
  cannot insert the same chat. In Mongo and not in Redis because no duplicated messages depends on this lock, and
  Redis evicts keys.

Every write is atomic per document (`find_one_and_update`, `update_many` with the state in the filter): two workers
never take the same job.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import BulkWriteError, DuplicateKeyError

from ...domain.infra.history_import import HistoryImportJob, JobStatus, QueueStats

JOBS_COLLECTION = "coexistence_import_jobs"
LEASES_COLLECTION = "coexistence_import_chat_leases"
TOP_ACTIVE_HINT = "idx_company_status_created"
_DUPLICATE_KEY = 11000


def _now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))


def _to_doc(job: HistoryImportJob) -> Dict[str, Any]:
    doc = job.model_dump(exclude={"id"})
    doc["status"] = job.status.value
    return doc


def _from_doc(doc: Dict[str, Any]) -> HistoryImportJob:
    return HistoryImportJob(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"})


def _oids(ids: List[str]) -> List[ObjectId]:
    return [ObjectId(i) for i in ids]


def top_active_companies_pipeline(limit: int) -> List[Dict[str, Any]]:
    """The companies with most pending work, answered by the index ALONE (covered plan: 0 documents read, verified
    with explain in dev). The three pieces are needed: the range on `company_id` (without it the index cannot tell an
    absent field from a null and fetches the document), the `$project` without `_id`, and the hint."""
    return [
        {"$match": {"company_id": {"$gte": ""}, "status": {"$in": [JobStatus.PENDING.value, JobStatus.RUNNING.value]}}},
        {"$project": {"_id": 0, "company_id": 1, "created_at": 1}},
        {"$group": {"_id": "$company_id", "jobs": {"$sum": 1}, "oldest": {"$min": "$created_at"}}},
        {"$sort": {"jobs": -1}},
        {"$limit": limit},
    ]


class MongoHistoryImportQueue:
    def __init__(self, collection):
        self.collection = collection

    async def enqueue(self, jobs: List[HistoryImportJob]) -> int:
        if not jobs:
            return 0
        try:
            result = await self.collection.insert_many([_to_doc(j) for j in jobs], ordered=False)
            return len(result.inserted_ids)
        except BulkWriteError as exc:
            errors = exc.details.get("writeErrors", [])
            if any(e.get("code") != _DUPLICATE_KEY for e in errors):
                raise
            return exc.details.get("nInserted", 0)

    async def claim(self, worker_id: str, lease: timedelta) -> Optional[HistoryImportJob]:
        now = _now()
        take = {"status": JobStatus.RUNNING.value, "worker_id": worker_id,
                "lease_until": now + lease, "updated_at": now}
        # First what a dead worker left taken —otherwise it waits behind the whole backlog— and with one more
        # attempt: a batch that kills the process cannot come back every 120 s forever.
        doc = await self.collection.find_one_and_update(
            {"status": JobStatus.RUNNING.value, "lease_until": {"$lt": now}},
            {"$set": take, "$inc": {"attempts": 1}},
            sort=[("created_at", 1)], return_document=ReturnDocument.AFTER,
        )
        if doc is None:
            doc = await self.collection.find_one_and_update(
                {"status": JobStatus.PENDING.value, "next_attempt_at": {"$lte": now}},
                {"$set": take},
                sort=[("created_at", 1)], return_document=ReturnDocument.AFTER,
            )
        return _from_doc(doc) if doc is not None else None

    async def claim_more_for_chat(
        self, job: HistoryImportJob, worker_id: str, lease: timedelta, max_messages: int
    ) -> List[HistoryImportJob]:
        now = _now()
        taken: List[HistoryImportJob] = []
        left = max_messages
        cursor = self.collection.find(
            {"company_id": job.company_id, "chat_key": job.chat_key,
             "status": JobStatus.PENDING.value, "next_attempt_at": {"$lte": now}},
            {"_id": 1, "n_messages": 1},
        ).sort("created_at", 1).limit(50)
        candidates = await cursor.to_list(length=50)
        for c in candidates:
            if c.get("n_messages", 0) > left:
                break
            doc = await self.collection.find_one_and_update(
                {"_id": c["_id"], "status": JobStatus.PENDING.value},
                {"$set": {"status": JobStatus.RUNNING.value, "worker_id": worker_id,
                          "lease_until": now + lease, "updated_at": now}},
                return_document=ReturnDocument.AFTER,
            )
            if doc is None:
                continue  # another worker took it in between
            taken.append(_from_doc(doc))
            left -= doc.get("n_messages", 0)
        return taken

    async def extend_lease(self, job_ids: List[str], worker_id: str, lease: timedelta) -> None:
        if not job_ids:
            return
        now = _now()
        await self.collection.update_many(
            {"_id": {"$in": _oids(job_ids)}, "status": JobStatus.RUNNING.value, "worker_id": worker_id},
            {"$set": {"lease_until": now + lease, "updated_at": now}},
        )

    async def release(self, job_ids: List[str], delay: timedelta) -> None:
        if not job_ids:
            return
        now = _now()
        await self.collection.update_many(
            {"_id": {"$in": _oids(job_ids)}, "status": JobStatus.RUNNING.value},
            {"$set": {"status": JobStatus.PENDING.value, "next_attempt_at": now + delay,
                      "lease_until": None, "worker_id": None, "updated_at": now}},
        )

    async def defer_chat(self, company_id: str, chat_key: str, delay: timedelta) -> None:
        now = _now()
        await self.collection.update_many(
            {"company_id": company_id, "chat_key": chat_key, "status": JobStatus.PENDING.value},
            {"$max": {"next_attempt_at": now + delay}, "$set": {"updated_at": now}},
        )

    async def complete(self, job_ids: List[str], imported: int, worker_id: str) -> None:
        if not job_ids:
            return
        now = _now()
        await self.collection.update_many(
            {"_id": {"$in": _oids(job_ids)}, "status": JobStatus.RUNNING.value, "worker_id": worker_id},
            {"$set": {"status": JobStatus.DONE.value, "done_at": now, "updated_at": now,
                      "lease_until": None, "last_error": None,
                      "batch_size": len(job_ids), "batch_imported": imported}},
        )

    async def retry_or_fail(self, job: HistoryImportJob, error: str, delay: Optional[timedelta]) -> None:
        now = _now()
        changes: Dict[str, Any] = {"last_error": error[:2000], "lease_until": None,
                                   "worker_id": None, "updated_at": now}
        if delay is None:
            changes["status"] = JobStatus.FAILED.value
        else:
            changes["status"] = JobStatus.PENDING.value
            changes["next_attempt_at"] = now + delay
        await self.collection.update_one(
            {"_id": ObjectId(job.id), "status": JobStatus.RUNNING.value, "worker_id": job.worker_id},
            {"$set": changes, "$inc": {"attempts": 1}},
        )

    async def stats(self, company_id: Optional[str] = None) -> QueueStats:
        base: Dict[str, Any] = {"company_id": company_id} if company_id else {}
        counts: Dict[str, int] = {}
        for status in (JobStatus.PENDING, JobStatus.RUNNING, JobStatus.FAILED, JobStatus.OVERFLOW):
            counts[status.value] = await self.collection.count_documents({**base, "status": status.value})
        oldest = await self.collection.find_one(
            {**base, "status": JobStatus.PENDING.value}, {"created_at": 1}, sort=[("created_at", 1)],
        )
        age = None
        if oldest is not None:
            created = oldest["created_at"]
            if created.tzinfo is None:
                created = created.replace(tzinfo=ZoneInfo("UTC"))
            age = max((_now() - created).total_seconds(), 0.0)
        return QueueStats(
            pending=counts["pending"], running=counts["running"], failed=counts["failed"],
            overflow=counts["overflow"], oldest_pending_s=age,
        )

    async def has_active(self, company_id: str, sync_id: Optional[str] = None) -> bool:
        query = {"company_id": company_id, "status": {"$in": [JobStatus.PENDING.value, JobStatus.RUNNING.value]}}
        if sync_id is not None:
            # Index `idx_company_sync_status`: without it this would FETCH the raw messages of every job.
            query["sync_id"] = str(sync_id)
        doc = await self.collection.find_one(query, {"_id": 1})
        return doc is not None

    async def top_active_companies(self, limit: int = 5) -> List[Dict[str, Any]]:
        cursor = self.collection.aggregate(top_active_companies_pipeline(limit), hint=TOP_ACTIVE_HINT)
        return [{"company_id": d["_id"], "jobs": d["jobs"], "oldest": d["oldest"]} async for d in cursor]


class MongoChatLeases:
    def __init__(self, collection):
        self.collection = collection

    async def acquire(self, key: str, owner: str, ttl: timedelta) -> bool:
        now = _now()
        try:
            await self.collection.insert_one({"_id": key, "owner": owner, "expires_at": now + ttl})
            return True
        except DuplicateKeyError:
            pass
        # It exists: it is taken only if it expired (a worker died holding the chat).
        doc = await self.collection.find_one_and_update(
            {"_id": key, "expires_at": {"$lt": now}},
            {"$set": {"owner": owner, "expires_at": now + ttl}},
        )
        return doc is not None

    async def extend(self, key: str, owner: str, ttl: timedelta) -> bool:
        result = await self.collection.update_one(
            {"_id": key, "owner": owner}, {"$set": {"expires_at": _now() + ttl}},
        )
        return result.matched_count == 1

    async def release(self, key: str, owner: str) -> None:
        await self.collection.delete_one({"_id": key, "owner": owner})
