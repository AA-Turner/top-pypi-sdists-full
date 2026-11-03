"""Users of a company («usuarios», with their roles and permissions): the port every user store implements.

The entity is `letschatty.models.company.assets.users.user.User`, unchanged: the person with their roles, their asset
permissions, their per-module overrides, their WhatsApp accounts and, for an integration, the hash of their API key.
A user and their permissions are one aggregate.

A read by id is not scoped to a company here: the authentication of every request reads the session's user by id,
and who may read or write which is decided by the caller.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol

from ...models.company.assets.users.user import User
from ...models.utils.types import StrObjectId


class UserRepository(Protocol):
    """Raises `NotFoundError` when the user does not exist."""

    async def get(self, user_id: StrObjectId) -> User:
        """Also a deleted one, and one of any company. Through the cache when there is one."""
        ...

    async def get_fresh(self, user_id: StrObjectId) -> User:
        """The same read without looking at the cache first (what the store has now), which refreshes the cache."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[User]: ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """JSON-ready preview dicts of the live users of the company, newest first."""
        ...

    async def add(self, user: User) -> User: ...

    async def update(self, user_id: StrObjectId, changes: User) -> User:
        """Writes the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def set_fields(self, company_id: StrObjectId, user_id: StrObjectId, fields: Dict[str, Any]) -> None:
        """`$set` of exactly `fields` (a `None` is written as null), without reading the user."""
        ...

    async def delete(self, user_id: StrObjectId) -> User:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...

    async def by_email_in_company(self, company_id: StrObjectId, email: str, live_only: bool) -> List[User]:
        """Exact match on `email` and `company_id`."""
        ...

    async def by_email(self, email: str, live_only: bool) -> List[User]:
        """Exact match on `email`, in every company."""
        ...

    async def live_by_email_ignoring_case(self, email: str) -> List[User]:
        """Live users, in every company, whose `email` is `email` ignoring case."""
        ...

    async def live_with_email_exists(self, company_id: StrObjectId, email: Optional[str]) -> bool: ...

    async def live_root(self, company_id: StrObjectId) -> Optional[User]:
        """The company's live user with `is_root`, or None."""
        ...

    async def pool_rows(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """The raw live rows of the company with only what the auto-assignment pool reads: `_id`, `roles`,
        `auto_assign_chats`, `user_type`, `status`, `account_ids`, `is_root`."""
        ...
