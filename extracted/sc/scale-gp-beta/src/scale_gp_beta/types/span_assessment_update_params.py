# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from .approval_status import ApprovalStatus
from .assessment_type import AssessmentType

__all__ = ["SpanAssessmentUpdateParams"]


class SpanAssessmentUpdateParams(TypedDict, total=False):
    approval: ApprovalStatus
    """Approval status (approved/rejected)"""

    assessment_type: AssessmentType
    """Type of assessment"""

    comment: str
    """Raw text feedback"""

    metadata: Dict[str, object]
    """Arbitrary JSON object for additional data"""

    overwrite: Dict[str, object]
    """User corrections to span output"""

    rating: int
    """Numerical rating (1-5)"""

    rubric: Dict[str, str]
    """Rule key-value pairs for rubric evaluation"""
