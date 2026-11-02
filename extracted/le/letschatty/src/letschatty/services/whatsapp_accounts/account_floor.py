"""The account floor: which WhatsApp accounts a person may see and act on.

One definition for every consumer (inbox lists, counters, search, open by id, assign, send...).
It is separate from the per-agent floor (`restricted_to_own_chats`): APB and `can_see_all_agents_chats`
do not lift it.

The floor is `None` (every account) or a list of account ids. A `None` entry in the list stands for the
chats with no `account_id`: until the migration stamps every chat they belong to the company's default
account, so the entry is added exactly when the user is allowed the default account.
"""
from typing import Any, Dict, List, Optional

from ...domain.whatsapp_accounts import Floor, chat_in_floor
from ...models.company.assets.users.user import User
from .chat_scope import chats_of_accounts

__all__ = ["Floor", "account_floor", "chat_in_floor", "floor_clause"]


def account_floor(user: User, default_account_id: Optional[str]) -> Floor:
    """None = no limit. Otherwise the allowed account ids (+ None when the default account is allowed)."""
    if not user.restricted_to_accounts:
        return None
    allowed: List[Optional[str]] = [account_id for account_id in (user.account_ids or [])]
    if default_account_id is not None and default_account_id in allowed:
        allowed.append(None)
    return allowed


def floor_clause(floor: Floor) -> Dict[str, Any]:
    """The Mongo filter of the floor: `{}` when there is none."""
    return {} if floor is None else chats_of_accounts(floor)
