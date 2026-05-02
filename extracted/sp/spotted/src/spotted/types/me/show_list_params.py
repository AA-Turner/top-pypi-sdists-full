# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ShowListParams"]


class ShowListParams(TypedDict, total=False):
    limit: int
    """The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50."""

    offset: int
    """The index of the first item to return.

    Default: 0 (the first item). Use with limit to get the next set of items.
    """
