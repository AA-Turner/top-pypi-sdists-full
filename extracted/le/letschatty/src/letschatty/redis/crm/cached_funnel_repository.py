"""Redis cache in front of any `FunnelRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, one set per collection, because the chat-in-a-funnel
code still reads them through the old services: `funnels:item:{id}`, `funnels:previews:{company}`,
`funnels:all:{company}` and the same with `funnel_stages:` (plus the global `…:all` lists). Every write invalidates
them; a cache failure never fails the request (ADR-006).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ...models.cache import CacheProtocol
from ...models.company.CRM.funnel import Funnel, FunnelStage
from ...models.utils.types import StrObjectId
from ...models.cache import CacheConfig
from ..cached_catalog_repository import CachedCatalogByIdWithPreviews


class CachedFunnelStageCatalog(CachedCatalogByIdWithPreviews[FunnelStage]):
    prefix = "funnel_stages"
    item_type = FunnelStage


class CachedFunnelRepository(CachedCatalogByIdWithPreviews[Funnel]):
    """The funnels' cache (`CachedCatalogByIdWithPreviews`, ADR-010 of api-chatty) and the stages', on `inner.stage_catalog`."""

    prefix = "funnels"
    item_type = Funnel

    def __init__(self, inner, cache: CacheProtocol, config: Optional[CacheConfig] = None, *,
                 stage_cache: Optional[CacheProtocol] = None, stage_config: Optional[CacheConfig] = None):
        """`cache`/`config` are the funnels' (the `Funnels` asset service's); `stage_cache`/`stage_config` the stages'
        (`FunnelStages`), the same ones when not given."""
        super().__init__(inner, cache, config)
        self.stage_catalog = CachedFunnelStageCatalog(inner.stage_catalog, cache if stage_cache is None else stage_cache,
                                                      config if stage_config is None else stage_config)

    async def get_stage(self, stage_id: StrObjectId) -> FunnelStage:
        return await self.stage_catalog.get(stage_id)

    async def list_stage_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        return await self.stage_catalog.list_previews(company_id)

    async def list_stages(self, company_id: StrObjectId) -> List[FunnelStage]:
        return await self.stage_catalog.list_live(company_id)

    async def add_stage(self, stage: FunnelStage) -> FunnelStage:
        return await self.stage_catalog.add(stage)

    async def update_stage(self, stage_id: StrObjectId, changes: FunnelStage) -> FunnelStage:
        return await self.stage_catalog.update(stage_id, changes)

    async def delete_stage(self, stage_id: StrObjectId) -> FunnelStage:
        return await self.stage_catalog.delete(stage_id)
