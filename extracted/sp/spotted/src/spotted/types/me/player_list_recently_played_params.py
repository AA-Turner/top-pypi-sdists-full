# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PlayerListRecentlyPlayedParams"]


class PlayerListRecentlyPlayedParams(TypedDict, total=False):
    after: int
    """A Unix timestamp in milliseconds.

    Returns all items after (but not including) this cursor position. If `after` is
    specified, `before` must not be specified.
    """

    before: int
    """A Unix timestamp in milliseconds.

    Returns all items before (but not including) this cursor position. If `before`
    is specified, `after` must not be specified.
    """

    limit: int
    """The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50."""
