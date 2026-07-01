# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

from .chat.sort_order import SortOrder

__all__ = ["EvaluationItemListParams"]


class EvaluationItemListParams(TypedDict, total=False):
    completion_status: Literal["failed", "passed", "all"]
    """Filter items by completion status.

    Pass 'failed' to return only items with errors, 'passed' for items without
    errors. Pass 'all' or omit to return all items.
    """

    ending_before: str

    evaluation_id: str

    include_archived: bool

    limit: int

    sort_by: str

    sort_order: SortOrder

    starting_after: str
