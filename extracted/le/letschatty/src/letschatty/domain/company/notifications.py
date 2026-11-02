"""Notifications of a company («notificaciones»): the banners of the home screen. The port every notification store
implements, and the rules of who sees one.

The entity is `letschatty.models.company.assets.notification.Notification`, unchanged. A notification is of one
company, or global (`company_id == GLOBAL_COMPANY_ID`): the same document is shown to every company. One about a
WhatsApp account (`account_id`) is shown only to who works that account.

A read by id is not scoped to a company here: a global one is everyone's, and who may read or write which is decided
by the caller with the rules below.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol

from ...models.company.assets.notification import GLOBAL_COMPANY_ID, Notification
from ...models.utils.types import StrObjectId
from ..whatsapp_accounts import chat_in_floor

#: The only fields the customer app sends when a person closes a banner.
DISMISS_FIELDS = frozenset({"dismissed", "dismissed_at"})


class NotificationRepository(Protocol):
    """Raises `NotFoundError` when the notification does not exist."""

    async def get(self, notification_id: StrObjectId) -> Notification:
        """Also a deleted one."""
        ...

    async def list_live(self, company_id: StrObjectId) -> List[Notification]:
        """The live notifications stored with that `company_id` (`GLOBAL_COMPANY_ID` = the global ones)."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """The same, as JSON-ready preview dicts (no `description`)."""
        ...

    async def add(self, notification: Notification) -> Notification: ...

    async def update(self, notification_id: StrObjectId, changes: Notification) -> Notification:
        """Writes the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def delete(self, notification_id: StrObjectId) -> Notification:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...


def is_global(notification: Notification) -> bool:
    return notification.company_id == GLOBAL_COMPANY_ID


def is_dismiss_only(changes: Any) -> bool:
    """The body of closing a banner: only `dismissed`/`dismissed_at` (a body that is not a dict never is)."""
    return isinstance(changes, dict) and set(changes.keys()).issubset(DISMISS_FIELDS)


def in_floor(notification: Dict[str, Any], allowed_account_ids: Optional[list]) -> bool:
    """A notification about one account is for who works that account; one without `account_id` is for everyone.
    `allowed_account_ids` is the person's floor (`None` = every account)."""
    account_id = notification.get("account_id")
    return not account_id or chat_in_floor(allowed_account_ids if isinstance(allowed_account_ids, list) else None,
                                           account_id if isinstance(account_id, str) else None)
