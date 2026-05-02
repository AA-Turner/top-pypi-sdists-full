# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .._types import SequenceNotStr
from .chat.sort_order import SortOrder

__all__ = ["EvaluationDashboardListParams"]


class EvaluationDashboardListParams(TypedDict, total=False):
    created_by_ids: SequenceNotStr[str]
    """Filter by creator user IDs"""

    ending_before: str

    evaluation_group_id: str

    evaluation_id: str

    include_archived: bool

    limit: int

    search: str
    """Search in name and tags"""

    sort_by: str

    sort_order: SortOrder

    starting_after: str

    tags: SequenceNotStr[str]
    """Filter by tags (case-insensitive)"""
