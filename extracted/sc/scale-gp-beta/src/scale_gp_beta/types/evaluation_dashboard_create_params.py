# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["EvaluationDashboardCreateParams"]


class EvaluationDashboardCreateParams(TypedDict, total=False):
    name: Required[str]
    """Dashboard name"""

    description: str
    """Optional description of the dashboard"""

    evaluation_group_id: str
    """Evaluation group ID (XOR with evaluation_id)"""

    evaluation_id: str
    """Evaluation ID (XOR with evaluation_group_id)"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""

    template_dashboard_id: str
    """Optional dashboard ID to use as template. Copies widget_order from template."""

    widget_order: SequenceNotStr[str]
    """Ordered array of widget IDs to display on this dashboard"""
