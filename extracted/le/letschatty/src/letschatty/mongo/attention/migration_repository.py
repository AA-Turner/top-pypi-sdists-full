"""`AttentionMigrationRepository` on `migraciones_de_atencion`: the same operations, filters and updates that
`company/assets/atencion_migracion/migraciones.py` of api-chatty ran: `find_one`s (the latest by `aplicada_at`, the
active one by state and `vence_at`, one by `_id`), an `update_many` that expires the overdue ones, an `insert_one` that
a duplicate on the unique partial index refuses, the targeted `update_one`s of the apply (`fallida`, `completa` +
`respuesta`, the `$push` of each thing created) and the conditional ones of the undo (`aplicada → deshaciendo`, and
taking it again after it stalled).

The stored shape is known only here: the Spanish keys, `_id` as an `ObjectId`, dates as Mongo returns them (without a
zone), `fuentes_antes[].campos` untouched. An id that is not an `ObjectId` reads and writes nothing.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Mapping, Optional

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from ...domain.attention.migrations import AttentionMigration, SourceCopy
from ...domain.attention.states import (MIGRATION_APPLIED, MIGRATION_EXPIRED, MIGRATION_FAILED, MIGRATION_UNDOING,
                                        MIGRATION_UNDONE)

COLLECTION = "migraciones_de_atencion"


def _oid(migration_id: Any) -> Optional[ObjectId]:
    if isinstance(migration_id, ObjectId):
        return migration_id
    try:
        return ObjectId(str(migration_id))
    except (InvalidId, TypeError):
        return None


def migration_of(document: Mapping[str, Any]) -> AttentionMigration:
    """The migration a stored document holds."""
    copies = tuple(
        SourceCopy(source_id=copy["source_id"], fields=copy.get("campos") or {}, absent=tuple(copy.get("ausentes") or ()))
        for copy in (document.get("fuentes_antes") or ()))
    return AttentionMigration(
        id=str(document["_id"]) if document.get("_id") is not None else None,
        company_id=document.get("company_id"), state=document.get("estado"), complete=bool(document.get("completa")),
        applied_at=document.get("aplicada_at"), expires_at=document.get("vence_at"),
        applied_by=document.get("aplicada_por"), body_hash=document.get("cuerpo_hash"), sources_before=copies,
        entries_created=tuple(document.get("entradas_creadas") or ()),
        reasons_created=tuple(document.get("motivos_creados") or ()), response=document.get("respuesta"))


def document_of(migration: AttentionMigration) -> Dict[str, Any]:
    """The stored shape of a migration that was just built, with the keys in the order `main` inserted them."""
    return {
        "_id": ObjectId(migration.id), "company_id": migration.company_id, "estado": migration.state,
        "completa": migration.complete, "aplicada_at": migration.applied_at, "vence_at": migration.expires_at,
        "aplicada_por": migration.applied_by, "cuerpo_hash": migration.body_hash,
        "fuentes_antes": [{"source_id": c.source_id, "campos": c.fields, "ausentes": list(c.absent)}
                          for c in migration.sources_before],
        "entradas_creadas": list(migration.entries_created), "motivos_creados": list(migration.reasons_created),
    }


class MongoAttentionMigrationRepository:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def latest(self, company_id: str) -> Optional[AttentionMigration]:
        document = await self.collection.find_one({"company_id": str(company_id)}, sort=[("aplicada_at", -1)])
        return None if document is None else migration_of(document)

    async def active(self, company_id: str, now: datetime) -> Optional[AttentionMigration]:
        document = await self.collection.find_one(
            {"company_id": str(company_id), "estado": {"$in": [MIGRATION_APPLIED, MIGRATION_UNDOING]},
             "vence_at": {"$gt": now}},
            sort=[("aplicada_at", -1)],
        )
        return None if document is None else migration_of(document)

    async def expire_overdue(self, company_id: str, now: datetime) -> None:
        await self.collection.update_many(
            {"company_id": str(company_id), "estado": {"$in": [MIGRATION_APPLIED, MIGRATION_UNDOING]},
             "vence_at": {"$lte": now}},
            {"$set": {"estado": MIGRATION_EXPIRED}},
        )

    async def open(self, migration: AttentionMigration) -> bool:
        try:
            await self.collection.insert_one(document_of(migration))
        except DuplicateKeyError:
            return False
        return True

    async def get(self, migration_id: str) -> Optional[AttentionMigration]:
        oid = _oid(migration_id)
        if oid is None:
            return None
        document = await self.collection.find_one({"_id": oid})
        return None if document is None else migration_of(document)

    async def mark_failed(self, migration_id: str) -> None:
        await self.collection.update_one({"_id": _oid(migration_id)}, {"$set": {"estado": MIGRATION_FAILED}})

    async def complete(self, migration_id: str, response: Dict[str, Any]) -> None:
        await self.collection.update_one({"_id": _oid(migration_id)}, {"$set": {"completa": True, "respuesta": response}})

    async def mark_undone(self, migration_id: str, now: datetime) -> None:
        await self.collection.update_one({"_id": _oid(migration_id)},
                                         {"$set": {"estado": MIGRATION_UNDONE, "deshecha_at": now}})

    async def record_created_reason(self, migration_id: str, reason_id: str) -> None:
        await self.collection.update_one({"_id": _oid(migration_id)}, {"$push": {"motivos_creados": reason_id}})

    async def record_created_entry(self, migration_id: str, entry_id: str) -> None:
        await self.collection.update_one({"_id": _oid(migration_id)}, {"$push": {"entradas_creadas": entry_id}})

    async def take_undo(self, migration_id: str, now: datetime) -> bool:
        result = await self.collection.update_one(
            {"_id": _oid(migration_id), "estado": MIGRATION_APPLIED},
            {"$set": {"estado": MIGRATION_UNDOING, "deshaciendo_at": now}},
        )
        return bool(getattr(result, "matched_count", 0))

    async def resume_undo(self, migration_id: str, now: datetime, stale_before: datetime) -> bool:
        result = await self.collection.update_one(
            {"_id": _oid(migration_id), "estado": MIGRATION_UNDOING, "deshaciendo_at": {"$lte": stale_before}},
            {"$set": {"deshaciendo_at": now}},
        )
        return bool(getattr(result, "matched_count", 0))
