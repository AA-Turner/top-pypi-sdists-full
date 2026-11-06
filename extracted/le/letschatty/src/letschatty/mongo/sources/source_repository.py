"""`SourceRepository` on the `sources` collection. Only Mongo: the cache is a decorator (ADR-001).

It reuses the asset collection the caller already has (api-chatty's, which writes `mapeo_motivo.at` as a date on
insert and on a whole-document update), so the stored document keeps exactly the shape analytics, copilot and
campaigns-lambda read. A read by id, the merge on update, the mark on delete and the restore are the catalog base's
(`MongoCatalogById`); the rest are the targeted reads and writes the attention flow needs, with the same filters,
projections and time limits as before.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId

from ...models.analytics.sources import SourceBase
from ...models.utils.types import StrObjectId
from ...services.factories.analytics.sources.source_factory import SourceFactory
from ..catalog_repository import MongoCatalogById

#: What the uniqueness checks read. Every required-without-default field of every source subclass is here: the
#: result is built into whole models (a missing `url` or `post_id` used to break every POST /sources).
VALIDATION_PROJECTION = {"_id": 1, "company_id": 1, "name": 1, "type": 1, "source_checker": 1, "trigger": 1, "ad_id": 1,
                         "topic_id": 1, "created_at": 1, "updated_at": 1, "template_name": 1, "url": 1,
                         "utm_campaign": 1, "meta_ad_id": 1, "google_ad_id": 1, "post_id": 1, "entrada_id": 1,
                         "account_id": 1}

#: What the motivos' mapping reads of a source.
MAPPING_PROJECTION = {
    "_id": 1, "name": 1, "type": 1, "created_at": 1, "motivo_ids": 1, "motivo_id": 1, "entrada_id": 1,
    "mapeo_motivo": 1, "meta_ad_id": 1, "google_ad_id": 1, "meta_headline": 1, "meta_body": 1, "headline": 1,
    "body": 1, "description": 1, "meta_ad_url": 1, "post_permalink": 1, "url": 1, "meta_media_type": 1,
    "media_type": 1,
}
MAPPING_MAX_TIME_MS = 10_000

_NOT_DECIDED_BY_A_PERSON = {"deleted_at": None, "mapeo_motivo.origen": {"$ne": "persona"}}
#: The query of each condition of `set_fields` (`domain/sources/sources.py`), as the motivos' mapping always wrote it.
CONDITIONS: Dict[str, Dict[str, Any]] = {
    "undecided_without_reasons": {**_NOT_DECIDED_BY_A_PERSON,
                                  "$or": [{"motivo_ids": {"$in": [None, []]}}, {"motivo_ids": {"$exists": False}}],
                                  "motivo_id": None},
    "undecided_without_mapping": {**_NOT_DECIDED_BY_A_PERSON, "mapeo_motivo": None},
    "pending_for_the_ai": {"deleted_at": None, "mapeo_motivo.origen": "ia", "mapeo_motivo.estado": "pendiente",
                           "motivo_ids": {"$in": [None, []]}, "motivo_id": None},
}


def _object_ids(ids: List[str]) -> List[ObjectId]:
    return [ObjectId(s) for s in ids]


class MongoSourceRepository(MongoCatalogById[SourceBase]):
    """`list_live` is the base's and always reads the store (`fresh` is the cache's concern)."""

    @property
    def _raw(self):
        """The Motor collection, for the targeted reads and writes."""
        return self.collection.collection

    async def list_for_validation(self, company_id: StrObjectId) -> List[SourceBase]:
        docs = await self.collection.get_projection_by_query(
            query={"company_id": str(company_id), "deleted_at": None}, projection=VALIDATION_PROJECTION)
        return [SourceFactory.instantiate_source(doc) for doc in docs]

    async def patch(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any]) -> None:
        await self.collection.partial_update(str(source_id), fields)

    # ── entradas ──

    async def entries_of_sources(self, company_id: StrObjectId) -> Dict[str, Optional[str]]:
        docs = await self.collection.get_projection_by_query(
            query={"company_id": str(company_id), "deleted_at": None}, projection={"_id": 1, "entrada_id": 1})
        return {str(d["_id"]): (str(d["entrada_id"]) if d.get("entrada_id") else None) for d in docs}

    async def accounts_of_sources(self, company_id: StrObjectId) -> Dict[str, Optional[str]]:
        docs = await self.collection.get_projection_by_query(
            query={"company_id": str(company_id), "deleted_at": None}, projection={"_id": 1, "account_id": 1})
        return {str(d["_id"]): (str(d["account_id"]) if d.get("account_id") else None) for d in docs}

    async def set_entry(self, company_id: StrObjectId, source_ids: List[str], entry_id: Optional[str],
                        now: datetime) -> int:
        result = await self._raw.update_many(
            {"_id": {"$in": _object_ids(source_ids)}, "company_id": str(company_id)},
            {"$set": {"entrada_id": str(entry_id) if entry_id else None, "updated_at": now}},
        )
        return int(getattr(result, "modified_count", 0) or 0)

    async def clear_entry(self, company_id: StrObjectId, entry_id: str, source_ids: Optional[List[str]],
                          now: datetime) -> List[str]:
        query: Dict[str, Any] = {"company_id": str(company_id), "entrada_id": str(entry_id)}
        if source_ids is not None:
            query["_id"] = {"$in": _object_ids(source_ids)}
        docs = await self.collection.get_projection_by_query(query=query, projection={"_id": 1})
        ids = [str(d["_id"]) for d in docs]
        if not ids:
            return []
        await self._raw.update_many(
            {**query, "_id": {"$in": _object_ids(ids)}},
            {"$set": {"entrada_id": None, "updated_at": now}},
        )
        return ids

    # ── motivos ──

    async def find_for_mapping(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[Dict[str, Any]]:
        return await self._raw.find_one(
            {"_id": ObjectId(str(source_id)), "company_id": str(company_id), "deleted_at": None},
            projection=MAPPING_PROJECTION, max_time_ms=MAPPING_MAX_TIME_MS,
        )

    async def mapping_candidates(self, company_id: StrObjectId, ad_types: List[str]) -> List[Dict[str, Any]]:
        cursor = self._raw.find(
            {"company_id": str(company_id), "deleted_at": None,
             "$or": [{"type": {"$in": list(ad_types)}}, {"mapeo_motivo.origen": "ia"}]},
            projection=MAPPING_PROJECTION,
        ).max_time_ms(MAPPING_MAX_TIME_MS)
        return await cursor.to_list(length=None)

    async def stored_fields(self, company_id: StrObjectId, source_ids: List[str],
                            fields: List[str]) -> List[Dict[str, Any]]:
        return await self.collection.get_projection_by_query(
            query={"_id": {"$in": _object_ids(source_ids)}, "company_id": str(company_id)},
            projection={"_id": 1, **{field: 1 for field in fields}})

    async def set_fields(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any],
                          when: Optional[str] = None) -> bool:
        condition = CONDITIONS[when] if when is not None else {}
        result = await self._raw.update_one(
            {"_id": ObjectId(str(source_id)), "company_id": str(company_id), **condition}, {"$set": fields})
        return bool(getattr(result, "matched_count", 0))

    async def put_back_fields(self, company_id: StrObjectId, source_id: StrObjectId, fields: Dict[str, Any],
                               absent: List[str]) -> None:
        changes: Dict[str, Any] = {}
        if fields:
            changes["$set"] = dict(fields)
        if absent:
            changes["$unset"] = {name: "" for name in absent}
        if not changes:
            return
        await self._raw.update_one({"_id": ObjectId(str(source_id)), "company_id": str(company_id)}, changes)

    # ── cache: nothing to drop here ──

    async def forget(self, company_id: StrObjectId, source_ids: List[str]) -> None:
        return None

    async def all_ids(self, company_id: StrObjectId) -> List[str]:
        docs = await self._raw.find({"company_id": company_id}, {"_id": 1}).to_list(length=None)
        return [str(d["_id"]) for d in docs]

    async def drop_cache(self, company_id: StrObjectId, source_ids: List[str]) -> None:
        return None
