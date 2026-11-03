"""`UserRepository` on the `users` collection: a catalog read by id (`MongoCatalogByIdWithPreviews`: the authentication
reads the session's user by id alone), plus the user's own queries by email, by root and for the auto-assignment pool.
Only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from ...models.company.assets.users.user import User, UserPreview
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogByIdWithPreviews

POOL_PROJECTION = {"_id": 1, "roles": 1, "auto_assign_chats": 1, "user_type": 1, "status": 1, "account_ids": 1,
                   "is_root": 1}


class MongoUserRepository(MongoCatalogByIdWithPreviews[User]):
    """Reuses the collection of the asset service, so the stored document keeps its shape (chatty-auth and the
    assignment lambda read it directly)."""

    def preview_projection(self) -> Dict[str, Any]:
        return UserPreview.get_projection()

    async def get_fresh(self, user_id: StrObjectId) -> User:
        return await self.get(user_id)

    async def set_fields(self, company_id: StrObjectId, user_id: StrObjectId, fields: Dict[str, Any]) -> None:
        await self.collection.partial_update(user_id, fields)

    def _users(self, rows: List[dict]) -> List[User]:
        return [self.collection.create_instance(row) for row in rows]

    async def by_email_in_company(self, company_id: StrObjectId, email: str, live_only: bool) -> List[User]:
        query = {"email": email, "company_id": company_id, **({"deleted_at": None} if live_only else {})}
        return self._users(await self.collection.collection.find(query).to_list(None))

    async def by_email(self, email: str, live_only: bool) -> List[User]:
        query = {"email": email, **({"deleted_at": None} if live_only else {})}
        return self._users(await self.collection.collection.find(query).to_list(None))

    async def live_by_email_ignoring_case(self, email: str) -> List[User]:
        """Anchored and escaped: test addresses use plus-addressing, and `+` is a regex quantifier."""
        query = {"email": {"$regex": f"^{re.escape(email)}$", "$options": "i"}, "deleted_at": None}
        return self._users(await self.collection.collection.find(query).to_list(None))

    async def live_with_email_exists(self, company_id: StrObjectId, email: Optional[str]) -> bool:
        found = await self.collection.collection.find_one({"email": email, "company_id": company_id, "deleted_at": None})
        return bool(found)

    async def live_root(self, company_id: StrObjectId) -> Optional[User]:
        row = await self.collection.collection.find_one({"company_id": company_id, "is_root": True, "deleted_at": None})
        return self.collection.create_instance(row) if row else None

    async def pool_rows(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        return await self.collection.collection.find({"company_id": company_id, "deleted_at": None},
                                                     projection=POOL_PROJECTION).to_list(None)
