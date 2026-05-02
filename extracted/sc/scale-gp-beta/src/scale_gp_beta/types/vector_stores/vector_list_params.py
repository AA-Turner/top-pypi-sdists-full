# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from ..chat.sort_order import SortOrder

__all__ = ["VectorListParams"]


class VectorListParams(TypedDict, total=False):
    cursor: str
    """Alias for starting_after. Use starting_after instead."""

    ending_before: str

    filter: str
    """Metadata filter expression (JSON)"""

    include_vectors: bool
    """Include embedding vectors"""

    limit: int

    sort_by: str

    sort_order: SortOrder

    starting_after: str
