"""`PendingEntryRepository` on `entradas_pendientes`: the same operations, filters, hints and time limits that
`company/chats/entrada_demorada.py` of api-chatty ran (`EntradasPendientes`): an `insert_one` that the unique partial
index turns into «already open», an `update_one` with `hint` to add a message, an atomic `find_one_and_update` to
claim, a projected `find_one`, `update_one`s to mark, close and fail, and a hinted `find` of the due ones.

The stored form lives only here: what a claim, a read and the due query answer is turned into the domain's
`PendingEntry`/`DuePendingEntry` (`pending_entry_from_stored`, `due_pending_entry_from_stored`)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from ...domain.attention.pending_entries import DuePendingEntry, PendingEntry
from ...domain.attention.states import (ENTRY_DONE as DONE, ENTRY_FAILED as FAILED, ENTRY_PENDING as PENDING,
                                        ENTRY_SENDING as SENDING)

COLLECTION = "entradas_pendientes"
UNIQUE_INDEX = "uniq_chat_abierta"
DUE_INDEX = "idx_abierta_proximo"
MAX_TIME_MS = 5_000
READ_PROJECTION = {"mensajes": 1, "procesados": 1, "contact_points": 1, "trazas": 1, "estado": 1, "company_id": 1,
                   "chat_id": 1, "intentos": 1, "due_at": 1, "demora_s": 1}



def _utc(t: Any) -> Optional[datetime]:
    """A stored date (Mongo answers it without a zone) in UTC; anything else, None."""
    if not isinstance(t, datetime):
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def _text(value: Any) -> Optional[str]:
    return None if value is None else str(value)


def _text_if_stored(doc: Dict[str, Any], key: str) -> Optional[str]:
    return str(doc[key]) if key in doc else None


def pending_entry_from_stored(doc: Dict[str, Any]) -> PendingEntry:
    """A stored entry (as a claim or a read answers it) as the domain's. Missing attempts are 0, the lists of message
    ids are kept as stored (the entry reads them when they are asked for) and so are the maps of contact points and
    traces (ENG-166)."""
    return PendingEntry(
        id=str(doc["_id"]), company_id=_text(doc.get("company_id")), chat_id=_text(doc.get("chat_id")),
        state=doc.get("estado"), attempts=int(doc.get("intentos") or 0), due_at=_utc(doc.get("due_at")),
        raw_messages=doc.get("mensajes"), raw_processed=doc.get("procesados"),
        contact_points=doc.get("contact_points") or {}, traces=doc.get("trazas") or {},
    )


def due_pending_entry_from_stored(doc: Dict[str, Any]) -> DuePendingEntry:
    """A due entry as the domain's: a missing company or chat is None (the sweep fails that entry alone), a stored null
    is the text "None", as `main` read them (`str(doc["company_id"])`)."""
    return DuePendingEntry(id=str(doc["_id"]), company_id=_text_if_stored(doc, "company_id"),
                           chat_id=_text_if_stored(doc, "chat_id"), next_at=_utc(doc.get("proximo_at")))


class MongoPendingEntryRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def open(self, company_id: str, *, chat_id: str, message_id: str, contact_point_id: Optional[str],
                   trace_id: Optional[str], delay_s: int, due_at: datetime, now: datetime) -> Optional[str]:
        item_id = ObjectId()
        doc = {
            "_id": item_id, "company_id": str(company_id), "chat_id": str(chat_id),
            "mensajes": [str(message_id)], "procesados": [],
            "contact_points": {str(message_id): str(contact_point_id) if contact_point_id else None},
            "trazas": {str(message_id): str(trace_id) if trace_id else None},
            "demora_s": int(delay_s), "due_at": due_at, "proximo_at": due_at, "estado": PENDING,
            "abierta": True, "intentos": 0, "creada_at": now,
        }
        try:
            await self.collection.insert_one(doc)
        except DuplicateKeyError:
            return None
        return str(item_id)

    async def add_message(self, chat_id: str, message_id: str, contact_point_id: Optional[str],
                          trace_id: Optional[str]) -> bool:
        mid = str(message_id)
        res = await self.collection.update_one(
            {"chat_id": str(chat_id), "abierta": True},
            {"$addToSet": {"mensajes": mid},
             "$set": {f"contact_points.{mid}": str(contact_point_id) if contact_point_id else None,
                      f"trazas.{mid}": str(trace_id) if trace_id else None}},
            hint=UNIQUE_INDEX,
        )
        return bool(res.matched_count)

    async def claim(self, item_id: str, *, due_by: datetime, now: datetime, lease_until: datetime,
                    claimed_by: str) -> Optional[PendingEntry]:
        doc = await self.collection.find_one_and_update(
            {"_id": ObjectId(item_id), "abierta": True,
             "$or": [{"estado": PENDING, "due_at": {"$lte": due_by}},
                     {"estado": SENDING, "lease_until": {"$lt": now}}]},
            {"$set": {"estado": SENDING, "lease_until": lease_until, "proximo_at": lease_until,
                      "reclamada_at": now, "reclamada_por": claimed_by},
             "$inc": {"intentos": 1}},
            return_document=ReturnDocument.AFTER,
            maxTimeMS=MAX_TIME_MS,
        )
        return None if doc is None else pending_entry_from_stored(doc)

    async def read(self, item_id: str) -> Optional[PendingEntry]:
        doc = await self.collection.find_one({"_id": ObjectId(item_id)}, projection=READ_PROJECTION,
                                             max_time_ms=MAX_TIME_MS)
        return None if doc is None else pending_entry_from_stored(doc)

    async def mark_processed(self, item_id: str, message_id: str, *, lease_until: datetime) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$addToSet": {"procesados": str(message_id)},
             "$set": {"lease_until": lease_until, "proximo_at": lease_until}},
        )

    async def close(self, item_id: str, *, messages: int, now: datetime) -> bool:
        res = await self.collection.update_one(
            {"_id": ObjectId(item_id), "estado": SENDING, "mensajes": {"$size": int(messages)}},
            {"$set": {"estado": DONE, "hecha_at": now}, "$unset": {"abierta": "", "proximo_at": ""}},
        )
        return bool(res.modified_count)

    async def fail(self, item_id: str, *, now: datetime, error: str) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"estado": FAILED, "hecha_at": now, "error": error},
             "$unset": {"abierta": "", "proximo_at": ""}},
        )

    async def due(self, *, until: datetime, limit: int) -> List[DuePendingEntry]:
        cursor = self.collection.find(
            {"abierta": True, "proximo_at": {"$lte": until}},
            projection={"_id": 1, "company_id": 1, "chat_id": 1, "proximo_at": 1},
        ).hint(DUE_INDEX).limit(int(limit)).max_time_ms(MAX_TIME_MS)
        return [due_pending_entry_from_stored(doc) for doc in (await cursor.to_list(length=int(limit)) or [])]
