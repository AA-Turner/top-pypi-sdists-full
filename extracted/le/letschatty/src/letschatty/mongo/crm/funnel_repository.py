"""`FunnelRepository` on the `funnels` and `funnel_stages` collections: two catalogs read by id (`MongoCatalogByIdWithPreviews`),
the funnels' and the stages' (`stage_catalog`). Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict, List

from ...models.company.CRM.funnel import Funnel, FunnelStage
from ...models.data_base.collection_interface import ChattyAssetCollectionInterface
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogByIdWithPreviews


class MongoFunnelStageCatalog(MongoCatalogByIdWithPreviews[FunnelStage]):
    def preview_projection(self) -> Dict[str, Any]:
        return FunnelStage.preview_class.get_projection()


class MongoFunnelRepository(MongoCatalogByIdWithPreviews[Funnel]):
    """The funnels' catalog; the stages' is `stage_catalog`. Reuses the collections the asset services were built on, so
    the stored documents keep their shape."""

    def __init__(self, funnels: ChattyAssetCollectionInterface, stages: ChattyAssetCollectionInterface):
        super().__init__(funnels)
        self.stage_catalog = MongoFunnelStageCatalog(stages)

    def preview_projection(self) -> Dict[str, Any]:
        return Funnel.preview_class.get_projection()

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
