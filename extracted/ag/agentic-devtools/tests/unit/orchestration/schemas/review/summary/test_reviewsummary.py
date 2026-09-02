"""Tests for ReviewSummary model."""

from agentic_devtools.orchestration.schemas.review.summary import ReviewSummary


class TestReviewSummary:
    """Tests for ReviewSummary construction and serialization."""

    def test_construction(self):
        summary = ReviewSummary(
            decision={
                "verdict": "approve",
                "confidence": 0.9,
                "rationale": "LGTM",
            },
            files_reviewed=3,
        )
        assert summary.files_reviewed == 3
        assert summary.decision.verdict.value == "approve"

    def test_defaults(self):
        summary = ReviewSummary(
            decision={
                "verdict": "approve",
                "confidence": 0.9,
                "rationale": "OK",
            },
        )
        assert summary.file_results == []
        assert summary.total_findings == 0
        assert summary.critical_findings == 0
        assert summary.files_reviewed == 0

    def test_model_dump(self):
        summary = ReviewSummary(
            decision={
                "verdict": "request_changes",
                "confidence": 0.7,
                "rationale": "Issues",
            },
            total_findings=5,
            critical_findings=1,
            files_reviewed=10,
        )
        data = summary.model_dump()
        assert data["total_findings"] == 5
        assert data["decision"]["verdict"] == "request_changes"

    def test_round_trip(self):
        original = ReviewSummary(
            decision={
                "verdict": "approve",
                "confidence": 0.95,
                "rationale": "Perfect",
            },
            files_reviewed=5,
        )
        raw = original.model_dump_json()
        restored = ReviewSummary.model_validate_json(raw)
        assert original == restored
