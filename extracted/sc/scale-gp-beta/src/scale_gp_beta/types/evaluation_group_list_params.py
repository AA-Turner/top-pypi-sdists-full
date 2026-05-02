# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .._types import SequenceNotStr
from .chat.sort_order import SortOrder
from .evaluation_group_views import EvaluationGroupViews

__all__ = ["EvaluationGroupListParams"]


class EvaluationGroupListParams(TypedDict, total=False):
    ending_before: str

    evaluation_id: str
    """Filter to groups containing this evaluation ID"""

    include_deleted: bool

    limit: int

    name: str

    sort_by: str

    sort_order: SortOrder

    starting_after: str

    tags: SequenceNotStr[str]

    views: List[EvaluationGroupViews]
    """Optional relationships to include: 'members', 'row_identifiers'"""
