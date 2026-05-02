# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["EvaluationDashboardUpdateParams"]


class EvaluationDashboardUpdateParams(TypedDict, total=False):
    description: str
    """Dashboard description"""

    name: str
    """Dashboard name"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""

    widget_order: SequenceNotStr[str]
    """Ordered array of widget IDs (for reordering widgets)"""
