# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["RatingQuestionConfiguration"]


class RatingQuestionConfiguration(BaseModel):
    max_label: str
    """Label shown for the maximum rating"""

    min_label: str
    """Label shown for the minimum rating"""

    steps: int
    """Number of discrete points on the scale (e.g., 5 for a 1–5 scale)"""
