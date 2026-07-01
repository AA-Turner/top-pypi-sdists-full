# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["CriterionUpdateParams"]


class CriterionUpdateParams(TypedDict, total=False):
    rubric_id: Required[str]

    annotations: Dict[str, object]
    """Free-form metadata for the Criteria"""

    title: str
    """The Criteria text"""

    weight: float
    """Weight multiplier for scoring"""
