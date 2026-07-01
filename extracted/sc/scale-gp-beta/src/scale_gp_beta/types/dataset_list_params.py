# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .._types import SequenceNotStr
from .chat.sort_order import SortOrder

__all__ = ["DatasetListParams"]


class DatasetListParams(TypedDict, total=False):
    ending_before: str

    include_archived: bool

    limit: int

    name: str

    sort_by: str

    sort_order: SortOrder

    starting_after: str

    tags: SequenceNotStr[str]
