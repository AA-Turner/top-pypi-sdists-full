# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .._types import SequenceNotStr
from .chat.sort_order import SortOrder
from .evaluation_views import EvaluationViews

__all__ = ["EvaluationListParams"]


class EvaluationListParams(TypedDict, total=False):
    ending_before: str

    include_archived: bool

    limit: int

    name: str

    sort_by: str

    sort_order: SortOrder

    starting_after: str

    tags: SequenceNotStr[str]

    views: List[EvaluationViews]
