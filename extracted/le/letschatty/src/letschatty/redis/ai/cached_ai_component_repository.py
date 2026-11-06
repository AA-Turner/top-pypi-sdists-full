"""Redis cache in front of any `AiComponentRepository` (ADR-001: the cache is a decorator).

Keys and TTLs are the ones the legacy `AiComponents` service always used, because other code still reads them:
`ai_components:item:{id}` and `ai_components:all:{company}`, 24 h. Adding, editing and deleting invalidate the item
and the company's and global lists (`AssetCache`, ADR-006); deleting test cases invalidates nothing.

The reads are not the asset service's: they are what `AiComponents` did on top of it, kept as in `main` and said to
`AssetCache` (ENG-68). The cached value is built with the component's own class, and a failed read of the cache is NOT
a miss: it raises (ENG-133). The list never reads the cache, it only leaves the company's list there.
"""
from __future__ import annotations

from typing import List

from ...models.base_models.ai_agent_component import AiAgentComponent
from ...models.utils.types import StrObjectId
from ...services.ai_components_service import AiComponentsService
from ..cached_catalog_repository import CachedCatalogRepository


class CachedAiComponentRepository(CachedCatalogRepository[AiAgentComponent]):
    prefix = "ai_components"
    item_type = AiAgentComponent
    build_cached = staticmethod(AiComponentsService.instantiate_component)
    raise_read_failures = True  # not caught, as in `main` (ENG-133)

    async def list_live(self, company_id: StrObjectId) -> List[AiAgentComponent]:
        return await self.assets.all(company_id, lambda: self.inner.list_live(company_id), ignore_cache=True)

    async def delete_test_cases_of_chat_example(self, company_id: StrObjectId, chat_example_id: StrObjectId) -> None:
        await self.inner.delete_test_cases_of_chat_example(company_id, chat_example_id)
