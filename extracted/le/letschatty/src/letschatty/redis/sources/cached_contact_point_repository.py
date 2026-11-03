"""Redis cache in front of any `ContactPointRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because other readers still read them:
`contact_points:item:{id}` and the company's and the global lists (`contact_points:all:{company}`…). The item key uses
the id as it was asked for, as before. Adding, editing and deleting invalidate them (ADR-006, `AssetCache`). A cache
failure never fails the request. Writing the creative clears only the item's key. A fresh read skips the cache read but still writes the item back, as the asset
service's `get_by_id(id, ignore_cache=True)` did. The reads by source and by chat go straight to Mongo.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from ...models.company.assets.contact_point import ContactPoint
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogById


class CachedContactPointRepository(CachedCatalogById[ContactPoint]):
    """A catalog's cache read by id (`CachedCatalogById`, ADR-010 of api-chatty) plus a fresh read and the queries."""

    prefix = "contact_points"
    item_type = ContactPoint

    async def get_fresh(self, contact_point_id: StrObjectId) -> ContactPoint:
        item = await self.inner.get_fresh(contact_point_id)
        try:
            await self.assets.cache.set(self.assets.item_key(contact_point_id),
                                        json.dumps(item.model_dump(by_alias=True, mode="json")),
                                        ttl=self.assets.config.cache_ttl)
        except Exception:
            pass  # silent, as the asset service's write after a read
        return item

    async def of_source(self, company_id: Optional[StrObjectId], source_id: StrObjectId) -> List[ContactPoint]:
        return await self.inner.of_source(company_id, source_id)

    async def of_chat(self, company_id: Optional[StrObjectId], chat_id: StrObjectId) -> List[ContactPoint]:
        return await self.inner.of_chat(company_id, chat_id)

    async def set_ad_creative(self, contact_point_id: StrObjectId, ad_creative: Dict[str, Any]) -> None:
        # Only the item, as the asset service's `partial_update` without `invalidate_previews`.
        await self.inner.set_ad_creative(contact_point_id, ad_creative)
        await self.assets.invalidate_item(contact_point_id)

    async def has_live_of_another_source(self, chat_id: StrObjectId, contact_point_id: StrObjectId,
                                         source_id: Optional[StrObjectId]) -> bool:
        return await self.inner.has_live_of_another_source(chat_id, contact_point_id, source_id)
