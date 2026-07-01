# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["RubricCriteriaInputParam"]


class RubricCriteriaInputParam(TypedDict, total=False):
    title: Required[str]
    """The Criteria text"""

    annotations: Dict[str, object]
    """Free-form metadata for the Criteria"""

    weight: float
    """Weight multiplier for scoring"""
