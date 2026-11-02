"""Which WhatsApp accounts (numbers) of a company an asset applies to.

`account_ids` on an asset (Motivo, Entrada) limits it to some accounts. EMPTY means ALL the
accounts of the company, the ones connected later included. That is the opposite of
`chats.account_id`, where a missing value means the DEFAULT account: an asset that never had a
scope keeps working for every number, and `make_default` does not move it.

Pure functions, no I/O. They never raise: a bad stored value must not break a whole
`get_all()` of the company (`get_docs` has no per-document guard).
"""
from typing import Any, Iterable, Optional

__all__ = ["normalize_account_ids", "applies_to_account", "scopes_overlap"]


def normalize_account_ids(value: Any) -> list[str]:
    """None / garbage -> []; strings only, no blanks, no duplicates, order kept.

    A bare string is ONE account id (`"A"` -> `["A"]`): iterating it would split it into characters
    and treating it as garbage would turn a scoped asset into "all accounts" - never widen."""
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if value is None or isinstance(value, (bytes, dict)):
        return []
    try:
        items: Iterable[Any] = list(value)
    except TypeError:
        return []
    seen: dict[str, None] = {}
    for item in items:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            seen.setdefault(text, None)
    return list(seen)


def applies_to_account(
    account_ids: Optional[Iterable[str]],
    account_id: Optional[str],
    default_account_id: Optional[str] = None,
) -> bool:
    """Does an asset scoped to `account_ids` apply to a chat of `account_id`?

    - empty scope -> True (every account);
    - a chat without `account_id` is the default account's: `default_account_id` is needed to
      answer, and without it a scoped asset does NOT apply (the caller logs; never "all").
    """
    scope = normalize_account_ids(account_ids)
    if not scope:
        return True
    effective = account_id or default_account_id
    return bool(effective) and str(effective) in scope


def scopes_overlap(first: Optional[Iterable[str]], second: Optional[Iterable[str]]) -> bool:
    """Can two assets scoped to `first` and `second` both apply to a chat of the same account?

    An empty scope is "every account", so it overlaps with anything; two scoped assets overlap only if they
    share an account. For the rules that compare assets with each other ("one phrase, one motivo")."""
    a, b = normalize_account_ids(first), normalize_account_ids(second)
    return not a or not b or bool(set(a) & set(b))
