"""Which account owns a chat, a topic, a source or a contact point.

ONE rule for everything that carries an `account_id` (cuentas por empresa): an owner WITHOUT
`account_id` belongs to the company's DEFAULT account. It is the rule `chats_of_account` has had since
the first stage; this module is where the other assets (topics, sources, contact points) read it from, so
there are not four copies of it that drift.

Pure functions, no I/O. They never raise: a bad stored value (garbage, a mock, an empty string) is an
absent value, because one malformed document must not break a whole `get_all()` of the company.
"""
from typing import Any, Optional

from .account_context import AccountContext

__all__ = ["stored_account_id", "belongs_to_account", "same_account"]


def stored_account_id(value: Any) -> Optional[str]:
    """The account id an owner carries, or None when it carries none (absent, null, empty, not a string)."""
    return value if isinstance(value, str) and value else None


def belongs_to_account(owner_account_id: Any, account: AccountContext) -> bool:
    """Does something owned by `owner_account_id` belong to `account`?

    An owner without account is the default account's: it belongs to `account` only when `account` is the
    default one. Mirrors `chats_of_account` (the Mongo filter) for in-memory objects."""
    owner = stored_account_id(owner_account_id)
    return owner == str(account.account_id) if owner else bool(account.is_default)


def same_account(first: Any, second: Any, default_account_id: Optional[str] = None) -> bool:
    """Do two owners belong to the same account? (a source and its topic, a contact point and a source).

    Two owners without account are both the default's. One without account is the default's, so it is the
    same as the other one only if that is the default account: that needs `default_account_id`. Without it
    the answer is True: when the default is unknown nobody can tell them apart, and the callers (uniqueness
    checks, «never mix accounts» guards) stay as they were before accounts instead of inventing a split."""
    a, b = stored_account_id(first), stored_account_id(second)
    if a and b:
        return a == b
    if not a and not b:
        return True
    if default_account_id is None:
        return True
    return (a or b) == str(default_account_id)
