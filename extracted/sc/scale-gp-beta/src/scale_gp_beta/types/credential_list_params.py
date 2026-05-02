# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .chat.sort_order import SortOrder

__all__ = ["CredentialListParams"]


class CredentialListParams(TypedDict, total=False):
    ending_before: str

    limit: int

    name: str
    """Filter credentials by name"""

    sort_by: str

    sort_order: SortOrder

    starting_after: str
