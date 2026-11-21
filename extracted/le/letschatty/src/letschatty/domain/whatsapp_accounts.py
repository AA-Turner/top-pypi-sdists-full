"""The rule of the account floor, with no infrastructure: what `services/whatsapp_accounts/account_floor.py` (which re-exports it), the
domain modules (notifications) and api-chatty's application layer share.

The floor is `None` (every account) or a list of account ids; a `None` entry stands for the chats with no
`account_id` (the company's default account).
"""
from typing import List, Optional

from ..models.company.assets.users.user import User

Floor = Optional[List[Optional[str]]]


def chat_in_floor(floor: Floor, chat_account_id: Optional[str]) -> bool:
    """May a person with this floor see a chat of `chat_account_id` (None = unstamped chat)?"""
    return floor is None or chat_account_id in floor


def account_floor(user: User, default_account_id: Optional[str]) -> Floor:
    """None = no limit. Otherwise the allowed account ids (+ None when the default account is allowed)."""
    if not user.restricted_to_accounts:
        return None
    allowed: List[Optional[str]] = [account_id for account_id in (user.account_ids or [])]
    if default_account_id is not None and default_account_id in allowed:
        allowed.append(None)
    return allowed
