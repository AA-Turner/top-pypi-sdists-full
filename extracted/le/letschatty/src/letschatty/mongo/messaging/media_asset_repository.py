"""`MediaAssetRepository` on the `media_assets` collection. Only Mongo: the cache is a decorator (ADR-001).

The listing is a keyset page on (`created_at`, `_id`); its cursor is this store's position, base64 of JSON. The
lookups by key and by hash always read Mongo, as the asset service's `get_by_query` did.
"""
from __future__ import annotations

import base64
import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId

from ...domain.messaging.media_assets import HIDDEN_BY_DEFAULT, MediaAssetFilter
from ...models.company.assets import MediaAsset
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.collections.media_asset_collection import MediaAssetCollection

# The legacy `MediaAssets` service's logger: the line stays as it was before the refactor.
logger = logging.getLogger("MediaAssets")


class MongoMediaAssetRepository:
    """Reuses `MediaAssetCollection`, so the stored document keeps exactly the shape the senders read."""

    def __init__(self, collection: MediaAssetCollection):
        self.collection = collection

    async def get(self, asset_id: StrObjectId) -> MediaAsset:
        return await self.collection.get_by_id(asset_id)

    async def page(self, company_id: StrObjectId, filter: MediaAssetFilter, descending: bool,
                   cursor: Optional[str], limit: int) -> Tuple[List[MediaAsset], Optional[str]]:
        query = self.query(company_id, filter)
        op = "$lt" if descending else "$gt"
        if cursor:
            try:
                c_created, c_id = decode_cursor(cursor)
                query["$or"] = [
                    {"created_at": {op: c_created}},
                    {"created_at": c_created, "_id": {op: c_id}},
                ]
            except Exception:
                logger.warning("invalid media cursor, starting from first page", exc_info=True)

        docs = await self.collection.collection.find(query).sort(sort_keys(descending)).limit(limit + 1).to_list(length=limit + 1)

        has_more = len(docs) > limit
        docs = docs[:limit]
        items = [self.collection.create_instance(d) for d in docs]
        next_cursor = encode_cursor(docs[-1]["created_at"], docs[-1]["_id"]) if (has_more and docs) else None
        return items, next_cursor

    @staticmethod
    def query(company_id: StrObjectId, filter: MediaAssetFilter) -> Dict[str, Any]:
        q: Dict[str, Any] = {"company_id": company_id, "deleted_at": None}
        if filter.type:
            q["type"] = filter.type
        if filter.folder is not None:
            q["folder"] = filter.folder
        # `$nin` also matches the old rows without an `origin` field.
        q["origin"] = filter.origin if filter.origin else {"$nin": list(HIDDEN_BY_DEFAULT)}
        if filter.starred:
            q["is_starred"] = True
        if filter.uploaded_by:
            q["uploaded_by"] = filter.uploaded_by
        if filter.search:
            q["name"] = {"$regex": re.escape(filter.search), "$options": "i"}
        return q

    async def find_by_s3_key(self, company_id: StrObjectId, s3_key: str) -> Optional[MediaAsset]:
        items = await self.collection.get_docs(query={"s3_key": s3_key, "deleted_at": None}, company_id=company_id)
        return items[0] if items else None

    async def find_by_sha256(self, company_id: StrObjectId, sha256: str) -> Optional[MediaAsset]:
        items = await self.collection.get_docs(query={"sha256": sha256, "deleted_at": None}, company_id=company_id)
        items.sort(key=lambda a: a.created_at)
        return items[0] if items else None

    async def add(self, asset: MediaAsset) -> MediaAsset:
        await self.collection.insert(asset)
        return asset

    async def edit(self, company_id: StrObjectId, asset_id: StrObjectId, fields: Dict[str, Any]) -> None:
        await self.collection.partial_update(asset_id, fields)

    async def record_use(self, asset_id: StrObjectId, use_count: int, last_used_at: datetime) -> None:
        await self.collection.partial_update(asset_id, {"use_count": use_count, "last_used_at": last_used_at})

    async def delete(self, asset_id: StrObjectId) -> MediaAsset:
        existing = await self.get(asset_id)
        await self.mark_deleted(asset_id)
        return existing

    async def mark_deleted(self, asset_id: StrObjectId) -> None:
        """Only the write: for the cache decorator, which already read it through the cache."""
        await self.collection.delete(asset_id)


def sort_keys(descending: bool) -> List[Tuple[str, int]]:
    """The listing's order; `idx_company_deleted_starred_created` ends with it (docs/media-assets-indexes.md)."""
    direction = -1 if descending else 1
    return [("created_at", direction), ("_id", direction)]


def encode_cursor(created_at: datetime, _id: Any) -> str:
    payload = {"created_at": created_at.isoformat(), "_id": str(_id)}
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()


def decode_cursor(token: str) -> Tuple[datetime, ObjectId]:
    data = json.loads(base64.urlsafe_b64decode(token.encode()).decode())
    return datetime.fromisoformat(data["created_at"]), ObjectId(data["_id"])
