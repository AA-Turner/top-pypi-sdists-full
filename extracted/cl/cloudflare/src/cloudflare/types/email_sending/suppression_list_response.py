# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["SuppressionListResponse", "Scope", "ScopeType", "ScopeUnionMember1"]


class ScopeType(BaseModel):
    type: Literal["account"]
    """Blocks the recipient for every sending domain of the account."""


class ScopeUnionMember1(BaseModel):
    type: Literal["sending_domain"]
    """Blocks the recipient only for mail whose envelope MAIL FROM uses `value`."""

    value: str
    """
    The sending domain: the domain part of the envelope MAIL FROM, lowercase,
    without a trailing dot.
    """


Scope: TypeAlias = Union[ScopeType, ScopeUnionMember1]


class SuppressionListResponse(BaseModel):
    id: str
    """Unique identifier for this suppression."""

    created_at: datetime
    """When the suppression was created."""

    email: str
    """The suppressed email address."""

    expires_at: Optional[datetime] = None
    """When the suppression expires. Null for a permanent suppression."""

    read_only: bool
    """Whether clients may mutate this suppression.

    This is determined by the server and must not be inferred from `reason`.
    """

    reason: str
    """
    Why the address is suppressed: `manual`, `complaint`, `hard_bounce`,
    `soft_bounce`, or `policy`.
    """

    note: Optional[str] = None
    """Advisory note for this suppression, if any."""

    scope: Optional[Scope] = None
    """
    Where the suppression applies: `account` for every sending domain of the
    account, or `sending_domain` for one envelope MAIL FROM domain.
    """
