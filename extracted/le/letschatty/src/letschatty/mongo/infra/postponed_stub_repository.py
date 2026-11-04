"""`PostponedStubRepository` on `postponed_stubs`: the same operations, filters, hint and time limits that
`meta_handler/postponed_stubs.py` of api-chatty ran (an `insert_one` that the unique wamid index turns into «already
stored», an atomic `find_one_and_update` to claim, an `update_one` to close, and a hinted `find` of the due ones)."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ...domain.infra.postponed_stubs import PENDING, RUNNING

COLLECTION = "postponed_stubs"
DUE_INDEX = "idx_open_next"
MAX_TIME_MS = 5_000


class MongoPostponedStubRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def add(self, *, wamid: str, phone_number_id: Optional[str], payload: Dict[str, Any], code: int,
                  due_at: datetime, now: datetime) -> Optional[str]:
        item_id = ObjectId()
        try:
            await self.collection.insert_one({
                "_id": item_id, "wamid": str(wamid), "phone_number_id": phone_number_id, "payload": payload,
                "code": int(code), "due_at": due_at, "next_at": due_at, "state": PENDING, "open": True,
                "attempts": 0, "created_at": now,
            })
        except DuplicateKeyError:
            return None
        return str(item_id)

    async def claim(self, item_id: str, *, due_by: datetime, now: datetime,
                    lease_until: datetime) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one_and_update(
            {"_id": ObjectId(item_id), "open": True,
             "$or": [{"state": PENDING, "due_at": {"$lte": due_by}},
                     {"state": RUNNING, "lease_until": {"$lt": now}}]},
            {"$set": {"state": RUNNING, "lease_until": lease_until, "next_at": lease_until, "claimed_at": now},
             "$inc": {"attempts": 1}},
            return_document=ReturnDocument.AFTER,
            maxTimeMS=MAX_TIME_MS,
        )

    async def close(self, item_id: str, *, state: str, now: datetime, error: Optional[str]) -> None:
        fields: Dict[str, Any] = {"state": state, "done_at": now}
        if error is not None:
            fields["error"] = error
        await self.collection.update_one({"_id": ObjectId(item_id)},
                                         {"$set": fields, "$unset": {"open": "", "next_at": ""}})

    async def due(self, *, until: datetime, limit: int) -> List[Dict[str, Any]]:
        cursor = self.collection.find(
            {"open": True, "next_at": {"$lte": until}}, projection={"_id": 1, "next_at": 1},
        ).hint(DUE_INDEX).limit(int(limit)).max_time_ms(MAX_TIME_MS)
        return list(await cursor.to_list(length=int(limit)) or [])
