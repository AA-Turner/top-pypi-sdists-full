# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["FollowingBulkRetrieveParams"]


class FollowingBulkRetrieveParams(TypedDict, total=False):
    type: Required[Literal["artist"]]
    """The ID type: currently only `artist` is supported."""

    after: str
    """The last artist ID retrieved from the previous request."""

    limit: int
    """The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50."""
