"""ReviewDecision model for structured LLM output schemas.

Provides the overall PR verdict (approve/request-changes) with confidence and rationale.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from .._confidence import ConfidenceScore
from .._enums import Verdict, normalize_verdict


class ReviewDecision(BaseModel):
    """Overall review decision for a pull request.

    Represents the final verdict after reviewing all files, including
    the confidence level in the decision and the supporting rationale.
    """

    verdict: Annotated[Verdict, BeforeValidator(normalize_verdict)] = Field(
        description="The review verdict: approve or request_changes"
    )
    confidence: ConfidenceScore = Field(description="Confidence level in the decision (0.0 to 1.0)")
    rationale: str = Field(description="Human-readable explanation of the decision")
    blocking_findings_count: int = Field(
        default=0,
        description="Number of high/critical findings that influenced the decision",
    )
