"""Redis cache in front of any `AiAgentRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used: `ai_agents:item:{id}`, `ai_agents:previews:{company}`,
`ai_agents:all:{company}` (and the global `…:all` lists), TTL from the caller (24 h). The fresh read writes the item
key, as the asset service's `get_by_id(ignore_cache=True)` did. Adding, editing (the compare-and-set only when it
wrote) and deleting invalidate them (ADR-006, `AssetCache`); a cache failure never fails the request. cintia-lambdas,
onboarding-intelligence and polls-lambda write the collection straight to Mongo and invalidate nothing: what they
write is seen when the keys expire.
"""
from __future__ import annotations

import json
from typing import Any, List, Optional, Tuple

from ...models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogWithPreviews


class CachedAiAgentRepository(CachedCatalogWithPreviews[ChattyAIAgent]):
    """A catalog's cache by company (`CachedCatalogWithPreviews`, ADR-010 of api-chatty) plus the fresh read, the
    compare-and-set and the lookup by calendar (never cached, as before)."""

    prefix = "ai_agents"
    item_type = ChattyAIAgent

    async def get_fresh(self, company_id: Optional[StrObjectId], agent_id: StrObjectId) -> ChattyAIAgent:
        """The asset service's `get_by_id(ignore_cache=True)`. The same copy lives in the entradas' and the users' caches
        (ENG-135: move it to `AssetCache`)."""
        agent = await self.inner.get_fresh(company_id, agent_id)
        try:
            await self.assets.cache.set(self.assets.item_key(agent_id),
                                        json.dumps(agent.model_dump(by_alias=True, mode="json")),
                                        ttl=self.assets.config.cache_ttl)
        except Exception:
            pass
        return agent

    async def stored_updated_at(self, company_id: StrObjectId, agent_id: StrObjectId) -> Tuple[bool, Any]:
        return await self.inner.stored_updated_at(company_id, agent_id)

    async def replace_if_unchanged(self, company_id: StrObjectId, agent: ChattyAIAgent, stored_updated_at: Any) -> bool:
        replaced = await self.inner.replace_if_unchanged(company_id, agent, stored_updated_at)
        if replaced:
            await self.assets.invalidate(agent.id, agent.company_id)
        return replaced

    async def company_ids_with_calendar(self, calendar_email: str) -> List[Any]:
        return await self.inner.company_ids_with_calendar(calendar_email)
