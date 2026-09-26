# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["SuppressionImportResponse", "Item", "ItemScope", "ItemScopeType", "ItemScopeUnionMember1"]


class ItemScopeType(BaseModel):
    type: Literal["account"]
    """Blocks the recipient for every sending domain of the account."""


class ItemScopeUnionMember1(BaseModel):
    type: Literal["sending_domain"]
    """Blocks the recipient only for mail whose envelope MAIL FROM uses `value`."""

    value: str
    """
    The sending domain: the domain part of the envelope MAIL FROM, lowercase,
    without a trailing dot.
    """


ItemScope: TypeAlias = Union[ItemScopeType, ItemScopeUnionMember1]


class Item(BaseModel):
    index: int
    """Zero-based index of this item in the request body."""

    status: Literal["processed", "invalid", "error", "skipped"]
    """Outcome for this item."""

    id: Optional[str] = None
    """The created or promoted suppression's identifier.

    Present when `status` is `processed`.
    """

    email: Optional[str] = None
    """The submitted email address for this item."""

    error: Optional[str] = None
    """Human-readable error message.

    Present when `status` is `invalid`, `error`, or `skipped`.
    """

    scope: Optional[ItemScope] = None
    """
    Where the suppression applies: `account` for every sending domain of the
    account, or `sending_domain` for one envelope MAIL FROM domain.
    """


class SuppressionImportResponse(BaseModel):
    deduplicated: int
    """
    Number of items dropped because their email address and scope repeated an
    earlier item in this request. Counted once and excluded from `items`.
    """

    errors: int
    """Number of items that failed to import due to an unexpected error."""

    invalid: int
    """Number of items with an invalid email address or sending domain."""

    items: List[Item]
    """Per-item results, in the same order as the request body."""

    processed: int
    """Number of items successfully created or promoted."""

    skipped: int
    """
    Number of items skipped because the existing suppression is not customer-managed
    (for example, a read-only policy suppression).
    """

    total: int
    """Total number of items in the request body, including duplicates."""
