"""Redis cache in front of any `UserRepository` (ADR-001: the cache is a decorator, not part of Mongo).

Keys are the ones the generic asset service has always used, because both still run side by side and every request's
authentication reads them: `users:item:{id}`, `users:previews:{company}`, `users:all:{company}` (and the global
`…:all` lists), with the asset service's TTLs. Every write invalidates them; a cache failure never fails the request.
Only the reads by id and the company lists are cached, as before: the queries by email, root and pool always reach
the store.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from ...models.company.assets.users.user import User
from ...models.utils.types import StrObjectId
from ..cached_catalog_repository import CachedCatalogByIdWithPreviews


class CachedUserRepository(CachedCatalogByIdWithPreviews[User]):
    prefix = "users"
    item_type = User

    async def get_fresh(self, user_id: StrObjectId) -> User:
        """The asset service's `get_by_id(ignore_cache=True)`: no cache read, and the store's answer written back (a
        failed write is silent)."""
        user = await self.inner.get_fresh(user_id)
        try:
            await self.assets.cache.set(self.assets.item_key(user_id),
                                        json.dumps(user.model_dump(by_alias=True, mode="json")),
                                        ttl=self.assets.config.cache_ttl)
        except Exception:
            pass
        return user

    async def set_fields(self, company_id: StrObjectId, user_id: StrObjectId, fields: Dict[str, Any]) -> None:
        """The asset service's `partial_update(…, invalidate_previews=True, company_id=…)`: the item and the lists."""
        await self.inner.set_fields(company_id, user_id, fields)
        await self.assets.invalidate(user_id, company_id)

    async def by_email_in_company(self, company_id: StrObjectId, email: str, live_only: bool) -> List[User]:
        return await self.inner.by_email_in_company(company_id, email, live_only)

    async def by_email(self, email: str, live_only: bool) -> List[User]:
        return await self.inner.by_email(email, live_only)

    async def live_by_email_ignoring_case(self, email: str) -> List[User]:
        return await self.inner.live_by_email_ignoring_case(email)

    async def live_with_email_exists(self, company_id: StrObjectId, email: Optional[str]) -> bool:
        return await self.inner.live_with_email_exists(company_id, email)

    async def live_root(self, company_id: StrObjectId) -> Optional[User]:
        return await self.inner.live_root(company_id)

    async def pool_rows(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        return await self.inner.pool_rows(company_id)
