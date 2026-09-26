# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["SuppressionDeleteResponse", "Scope", "ScopeType", "ScopeUnionMember1"]


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


class SuppressionDeleteResponse(BaseModel):
    id: str
    """The suppression's identifier."""

    scope: Optional[Scope] = None
    """
    Where the suppression applies: `account` for every sending domain of the
    account, or `sending_domain` for one envelope MAIL FROM domain.
    """
