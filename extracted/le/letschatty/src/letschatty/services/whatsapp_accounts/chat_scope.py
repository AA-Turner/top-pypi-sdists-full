"""The chats of one account, as a Mongo filter.

R1 of the design: without a chat id, a chat is looked up by `{company_id, account_id, person}`,
never by company and person alone. Until the backfill (M2) stamps `account_id` on every chat,
the company's DEFAULT account also owns the chats that have none — at that point a company has
exactly one account, so those chats can only be its.
"""
from typing import Any, Dict, Iterable, Optional

from ...models.whatsapp.account_context import AccountContext


def chats_of_account(account: AccountContext) -> Dict[str, Any]:
    if account.is_default:
        return {"$or": [{"account_id": account.account_id}, {"account_id": {"$exists": False}}]}
    return {"account_id": account.account_id}


def chats_of_accounts(account_ids: Iterable[Optional[str]]) -> Dict[str, Any]:
    """The chats of several accounts, as ONE field with `$in` (never an `$or`: it keeps the index order).

    A `None` entry matches the chats with no `account_id` (`$in` with null matches a missing field), which
    is how "a chat without account is the default account's" travels in the account floor.
    """
    return {"account_id": {"$in": list(account_ids)}}
