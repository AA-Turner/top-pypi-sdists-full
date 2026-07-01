# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["RatingQuestionConfigurationParam"]


class RatingQuestionConfigurationParam(TypedDict, total=False):
    max_label: Required[str]
    """Label shown for the maximum rating"""

    min_label: Required[str]
    """Label shown for the minimum rating"""

    steps: Required[int]
    """Number of discrete points on the scale (e.g., 5 for a 1–5 scale)"""
