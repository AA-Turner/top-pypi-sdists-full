"""ReviewSummary model for structured LLM output schemas.

Provides the aggregated review summary across all files in a PR.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .decision import ReviewDecision
from .result import FileReviewResult


class ReviewSummary(BaseModel):
    """Aggregated review summary across all files in a pull request.

    Combines individual file results with an overall decision and
    statistics about the review outcome.
    """

    decision: ReviewDecision = Field(description="The overall review decision for the PR")
    file_results: list[FileReviewResult] = Field(
        default_factory=list,
        description="Individual review results per file",
    )
    total_findings: int = Field(default=0, description="Total number of findings across all files")
    critical_findings: int = Field(
        default=0,
        description="Number of critical-severity findings",
    )
    files_reviewed: int = Field(default=0, description="Number of files reviewed")
