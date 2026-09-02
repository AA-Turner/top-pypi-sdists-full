"""Tests for suppressed_findings in the defer_suppressed module."""

from __future__ import annotations

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.defer_suppressed import suppressed_findings
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_SUPPRESSED_COMMENTS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot

REVIEW_BODY = """### Comments suppressed due to low confidence (1)

**specs/3672-deferral/spec.md**

The acceptance criteria are ambiguous here.
"""


def _verdict(review_id: int = 42) -> CopilotGateVerdict:
    return CopilotGateVerdict(
        passed=False,
        reason=REASON_SUPPRESSED_COMMENTS,
        review_id=review_id,
        body_comment_count=0,
        suppressed_count=1,
    )


class TestSuppressedFindings:
    """Tests for suppressed_findings."""

    def test_returns_entries_of_the_evaluated_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            reviews=[
                ReviewInfo(id=7, user="Copilot", state="COMMENTED", body="unrelated"),
                ReviewInfo(id=42, user="Copilot", state="COMMENTED", body=REVIEW_BODY),
            ],
            copilot_gate_verdict=_verdict(42),
        )
        findings = suppressed_findings(snapshot)
        assert [path for path, _ in findings] == ["specs/3672-deferral/spec.md"]
        assert "ambiguous" in findings[0][1]

    def test_returns_empty_when_review_not_in_snapshot(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, reviews=[], copilot_gate_verdict=_verdict(42))
        assert suppressed_findings(snapshot) == []

    def test_returns_empty_without_verdict(self) -> None:
        assert suppressed_findings(PRStateSnapshot(pr_number=1)) == []

    def test_returns_empty_without_review_id(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, copilot_gate_verdict=_verdict(0))
        assert suppressed_findings(snapshot) == []
