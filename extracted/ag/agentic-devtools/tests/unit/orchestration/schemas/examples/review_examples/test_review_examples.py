"""Tests for review domain example factories."""

from agentic_devtools.orchestration.schemas.examples import (
    make_code_suggestion,
    make_file_review_finding,
    make_file_review_result,
    make_review_decision,
    make_review_summary,
)
from agentic_devtools.orchestration.schemas.review import (
    CodeSuggestion,
    FileReviewFinding,
    FileReviewResult,
    ReviewDecision,
    ReviewSummary,
)


class TestReviewExamples:
    """Tests for review domain example factories."""

    def test_make_code_suggestion_returns_valid(self):
        result = make_code_suggestion()
        assert isinstance(result, CodeSuggestion)
        assert result.file_path != ""

    def test_make_file_review_finding_returns_valid(self):
        result = make_file_review_finding()
        assert isinstance(result, FileReviewFinding)

    def test_make_file_review_result_returns_valid(self):
        result = make_file_review_result()
        assert isinstance(result, FileReviewResult)

    def test_make_review_decision_returns_valid(self):
        result = make_review_decision()
        assert isinstance(result, ReviewDecision)

    def test_make_review_summary_returns_valid(self):
        result = make_review_summary()
        assert isinstance(result, ReviewSummary)

    def test_factories_return_new_instances(self):
        a = make_code_suggestion()
        b = make_code_suggestion()
        assert a is not b
        assert a == b  # Same content but different objects

    def test_kwargs_override(self):
        result = make_code_suggestion(file_path="custom/path.py")
        assert result.file_path == "custom/path.py"
