# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .evaluation_group_views import EvaluationGroupViews

__all__ = ["EvaluationGroupRetrieveParams"]


class EvaluationGroupRetrieveParams(TypedDict, total=False):
    include_deleted: bool

    views: List[EvaluationGroupViews]
    """Optional relationships to include: 'members', 'row_identifiers'"""
