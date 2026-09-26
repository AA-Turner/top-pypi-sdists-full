# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo

__all__ = ["SuppressionImportParams", "Item", "ItemScope", "ItemScopeType", "ItemScopeUnionMember1"]


class SuppressionImportParams(TypedDict, total=False):
    account_id: Required[str]
    """Cloudflare account ID."""

    items: Required[Iterable[Item]]
    """Suppressions to import.

    Items with the same email address and scope are deduplicated before processing.
    """


class ItemScopeType(TypedDict, total=False):
    type: Required[Literal["account"]]
    """Blocks the recipient for every sending domain of the account."""


class ItemScopeUnionMember1(TypedDict, total=False):
    type: Required[Literal["sending_domain"]]
    """Blocks the recipient only for mail whose envelope MAIL FROM uses `value`."""

    value: Required[str]
    """The sending domain to suppress for: the domain part of the envelope MAIL FROM.

    It is lowercased and trailing dots are removed. Internationalized domains must
    use the ASCII (punycode) form. Ownership is not checked; a domain the account
    does not send from never matches.
    """


ItemScope: TypeAlias = Union[ItemScopeType, ItemScopeUnionMember1]


class Item(TypedDict, total=False):
    email: Required[str]
    """The email address to suppress."""

    expires_at: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Expiration timestamp for the suppression.

    Omit or set to null for a permanent suppression that never expires.
    """

    note: str
    """Advisory note for this suppression. Not enforced or validated beyond length."""

    scope: ItemScope
    """Where the suppression applies.

    Omit for `{ "type": "account" }`, which blocks the recipient for every sending
    domain of the account.
    """
