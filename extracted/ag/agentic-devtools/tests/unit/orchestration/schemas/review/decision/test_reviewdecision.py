"""Tests for ReviewDecision model."""

from agentic_devtools.orchestration.schemas._enums import Verdict
from agentic_devtools.orchestration.schemas.review.decision import ReviewDecision


class TestReviewDecision:
    """Tests for ReviewDecision construction and serialization."""

    def test_construction(self):
        decision = ReviewDecision(
            verdict="approve",
            confidence=0.95,
            rationale="All tests pass",
        )
        assert decision.verdict == Verdict.APPROVE
        assert decision.confidence == 0.95
        assert decision.blocking_findings_count == 0

    def test_case_insensitive_verdict(self):
        decision = ReviewDecision(
            verdict="REQUEST_CHANGES",
            confidence=0.8,
            rationale="Issues found",
        )
        assert decision.verdict == Verdict.REQUEST_CHANGES

    def test_confidence_int_coercion(self):
        decision = ReviewDecision(
            verdict="approve",
            confidence=1,
            rationale="Perfect",
        )
        assert decision.confidence == 1.0

    def test_model_dump(self):
        decision = ReviewDecision(
            verdict="approve",
            confidence=0.9,
            rationale="LGTM",
            blocking_findings_count=0,
        )
        data = decision.model_dump()
        assert data["verdict"] == "approve"
        assert data["confidence"] == 0.9

    def test_confidence_for_policy_evaluation(self):
        """Verify confidence field enables direct conditional evaluation."""
        decision = ReviewDecision(
            verdict="approve",
            confidence=0.92,
            rationale="Good",
        )
        # Should work directly as float comparison
        assert decision.confidence >= 0.9
        assert decision.confidence < 1.0
