# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .evaluation_views import EvaluationViews

__all__ = ["EvaluationRetrieveParams"]


class EvaluationRetrieveParams(TypedDict, total=False):
    include_archived: bool

    views: List[EvaluationViews]
