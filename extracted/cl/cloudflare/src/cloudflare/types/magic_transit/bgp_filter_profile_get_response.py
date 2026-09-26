# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BGPFilterProfileGetResponse"]


class BGPFilterProfileGetResponse(BaseModel):
    id: str
    """Identifier"""

    description: str
    """Description of the filter profile"""

    match_action: Literal["allow", "deny"]
    """Action to take when a route matches one of the targets in this profile"""

    name: str
    """Friendly name for the filter profile"""

    targets: List[str]
    """List of CIDR prefixes.

    Each entry may carry an optional suffix that specifies which prefix lengths to
    match relative to the prefix length N: '{X,Y}' matches prefix lengths in the
    inclusive range [X, Y] where N <= X <= Y <= max (max is 32 for IPv4, 128 for
    IPv6), '{X}' matches exactly length X (equivalent to {X,X}), '+' is shorthand
    for {N, max} (the prefix and all more-specific subnets, including at length N
    itself; valid even when N is the maximum length). Omit the suffix to match the
    prefix exactly at length N.
    """

    created_on: Optional[datetime] = None

    modified_on: Optional[datetime] = None
