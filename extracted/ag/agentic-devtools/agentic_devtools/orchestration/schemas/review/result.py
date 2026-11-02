"""FileReviewResult model for structured LLM output schemas.

Provides the complete result of reviewing a single file in a PR.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .finding import FileReviewFinding

# This node emits only ``approved`` / ``needs-work`` for reviewable files.
# Non-reviewable files (FR-011) use the minimal ``approved`` result shape rather
# than a terminal ``skipped`` status, so ``skipped`` is intentionally excluded.
ReviewStatus = Literal["approved", "needs-work"]


class FileReviewResult(BaseModel):
    """Complete review result for a single file in a pull request.

    Aggregates all findings for a file along with an overall status
    and human-readable summary of the review outcome.
    """

    file_path: str = Field(description="Path to the reviewed file")
    status: ReviewStatus = Field(description="Review status: 'approved' or 'needs-work'")
    summary: str = Field(description="Human-readable summary of the file review")
    findings: list[FileReviewFinding] = Field(
        default_factory=list,
        description="List of findings identified during review",
    )
