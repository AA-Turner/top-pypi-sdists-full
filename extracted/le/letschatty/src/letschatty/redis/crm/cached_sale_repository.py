"""Redis cache in front of any `SaleRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because both still run side by side and the
chat's readers go through it: `sales:item:{id}` (and the company and global lists, which nobody reads
today but the asset service still fills). The order-number lookup is never cached: it decides a 409.
Only the edit invalidates, as in `main`: the register and the delete clear nothing. A cache failure never fails the
request.
"""
from __future__ import annotations

from typing import List, Optional

from ...domain.crm.sales import SaleRepository
from ...models.cache import CacheProtocol
from ...models.company.assets.sale import Sale
from ...models.utils.types import StrObjectId
from ...models.cache import CacheConfig
from ..asset_cache import AssetCache


class CachedSaleRepository:
    def __init__(self, inner: SaleRepository, cache: CacheProtocol, config: Optional[CacheConfig] = None):
        self.inner = inner
        self.assets = AssetCache("sales", Sale, cache, config)

    async def get(self, company_id: StrObjectId, sale_id: StrObjectId) -> Sale:
        return await self.assets.item(sale_id, lambda: self.inner.get(company_id, sale_id))

    async def find_live_by_crm_id(self, company_id: StrObjectId, crm_id: str, limit: int) -> List[Sale]:
        return await self.inner.find_live_by_crm_id(company_id, crm_id, limit)

    async def add(self, sale: Sale) -> Sale:
        # As in `main` (`SalesEditor`): the register goes straight to the collection and clears nothing.
        return await self.inner.add(sale)

    async def save(self, sale: Sale) -> Sale:
        saved = await self.inner.save(sale)
        await self.assets.invalidate(saved.id, saved.company_id)
        return saved

    async def delete(self, company_id: StrObjectId, sale_id: StrObjectId) -> None:
        # As in `main`: the delete clears nothing, so a deleted sale stays cached alive until its TTL (ENG-70, kept).
        await self.inner.delete(company_id, sale_id)
