# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .assessment_type import AssessmentType

__all__ = ["SpanAssessmentListParams"]


class SpanAssessmentListParams(TypedDict, total=False):
    assessment_type: AssessmentType
    """Filter by assessment type"""

    span_id: str
    """Filter by span ID.

    Either span_id or trace_id must be provided as a query parameter.
    """

    trace_id: str
    """Filter by trace ID.

    Either span_id or trace_id must be provided as a query parameter.
    """
