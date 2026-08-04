# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .chat.sort_order import SortOrder

__all__ = ["BuildListParams"]


class BuildListParams(TypedDict, total=False):
    agent_name: str
    """Filter builds by agent name"""

    ending_before: str

    limit: int

    sort_by: str

    sort_order: SortOrder

    source_commit: str
    """Filter builds by source git commit"""

    starting_after: str

    working_tree_hash: str
    """Filter builds by build-context content hash"""
