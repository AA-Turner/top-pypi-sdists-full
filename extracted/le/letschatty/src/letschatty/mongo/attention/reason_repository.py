"""`ReasonRepository` on the `motivos` collection: a catalog read by id (`MongoCatalogByIdWithPreviews`) plus the fresh
read and the live «Consulta general» of a company. Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from typing import Any, Dict, List

from ...models.company.assets.motivo import Motivo, MotivoPreview
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogByIdWithPreviews


class MongoReasonRepository(MongoCatalogByIdWithPreviews[Motivo]):
    """Reuses the asset collection of the legacy `Motivos` service, so the stored document keeps its shape (the
    cintia-lambdas read it straight from Mongo)."""

    def preview_projection(self) -> Dict[str, Any]:
        return MotivoPreview.get_projection()

    async def get_fresh(self, reason_id: StrObjectId) -> Motivo:
        return await self._read(reason_id)

    async def list_fallbacks(self, company_id: StrObjectId) -> List[Motivo]:
        # The collection's own `get_by_query`, as the service did: the company as text in the query, not the helper's
        # company filter.
        return await self.collection.get_by_query(
            query={"company_id": str(company_id), "is_fallback": True, "deleted_at": None})

    async def has_general_inquiry(self, company_id: StrObjectId, *, max_time_ms: int) -> bool:
        found = await self.collection.collection.find_one(
            {"company_id": str(company_id), "is_fallback": True, "deleted_at": None}, projection={"_id": 1},
            max_time_ms=max_time_ms)
        return found is not None
