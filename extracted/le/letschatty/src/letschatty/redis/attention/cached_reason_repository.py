"""Redis cache in front of any `ReasonRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because the legacy `Motivos` service still serves the
readers (`get_all`, `get_by_id`: the attention runtime and the sources) on the same keys: `motivos:item:{id}`,
`motivos:previews:{company}`, `motivos:all:{company}` (and the global `…:all` lists). The fresh read writes the item key,
as the asset service's `get_by_id(ignore_cache=True)` did. Adding, editing and deleting invalidate them (ADR-006,
`AssetCache`). A cache failure never fails the request.
"""
from __future__ import annotations

import json
from typing import List

from ...models.company.assets.motivo import Motivo
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogByIdWithPreviews


class CachedReasonRepository(CachedCatalogByIdWithPreviews[Motivo]):
    """A catalog's cache read by id (`CachedCatalogByIdWithPreviews`, ADR-010 of api-chatty) plus the fresh read and the
    live «Consulta general», which is never cached."""

    prefix = "motivos"
    item_type = Motivo

    async def get_fresh(self, reason_id: StrObjectId) -> Motivo:
        reason = await self.inner.get_fresh(reason_id)
        try:
            await self.assets.cache.set(self.assets.item_key(reason_id),
                                        json.dumps(reason.model_dump(by_alias=True, mode="json")),
                                        ttl=self.assets.config.cache_ttl)
        except Exception:
            pass
        return reason

    async def list_fallbacks(self, company_id: StrObjectId) -> List[Motivo]:
        return await self.inner.list_fallbacks(company_id)
