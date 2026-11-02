"""`SaleRepository` on the `sales` collection. Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import List

from ...models.company.assets.sale import Sale
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.collections.sale_collection import SaleCollection


class MongoSaleRepository:
    """Reuses `SaleCollection`, so the stored document has exactly the shape analytics and the other
    services read (`sold_at` as a date, `items`, the derived `product_id`)."""

    def __init__(self, collection: SaleCollection):
        self.collection = collection

    async def get(self, company_id: StrObjectId, sale_id: StrObjectId) -> Sale:
        # Not filtered by company: the use case checks it (ADR-007, ENG-10).
        return await self.collection.get_by_id(sale_id)

    async def find_live_by_crm_id(self, company_id: StrObjectId, crm_id: str, limit: int) -> List[Sale]:
        # Index `idx_company_crm_id` (api-chatty `Database/indexes/sales_indexes.py`).
        return await self.collection.get_docs(company_id=company_id, query={"crm_id": crm_id, "deleted_at": None}, limit=limit)

    async def add(self, sale: Sale) -> Sale:
        await self.collection.insert(sale)
        return sale

    async def save(self, sale: Sale) -> Sale:
        # Merged onto what is in Mongo now, writing only what changed (`UpdateableMixin.merge`).
        existing = await self.collection.get_by_id(sale.id)
        merged, sent_fields = existing.merge(sale)
        await self.collection.update_fields(merged, sent_fields)
        return merged

    async def delete(self, company_id: StrObjectId, sale_id: StrObjectId) -> None:
        await self.collection.delete(sale_id)
