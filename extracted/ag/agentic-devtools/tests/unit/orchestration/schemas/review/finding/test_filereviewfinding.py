"""Tests for FileReviewFinding model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.orchestration.schemas._enums import Severity
from agentic_devtools.orchestration.schemas.review.finding import (
    CodeSuggestion,
    FileReviewFinding,
)


class TestFileReviewFinding:
    """Tests for FileReviewFinding construction and serialization."""

    def test_construction(self):
        finding = FileReviewFinding(
            severity="high",
            description="Missing null check",
            diff_side="new",
            new_line=42,
            confidence=0.8,
        )
        assert finding.severity == Severity.HIGH
        assert finding.diff_side == "new"
        assert finding.new_line == 42
        assert finding.old_line is None
        assert finding.suggestion is None

    def test_with_suggestion(self):
        suggestion = CodeSuggestion(
            file_path="f.py",
            start_line=1,
            end_line=1,
            original_code="a",
            replacement_code="b",
        )
        finding = FileReviewFinding(
            severity="medium",
            description="test",
            diff_side="new",
            new_line=1,
            confidence=0.8,
            suggestion=suggestion,
        )
        assert finding.suggestion is not None
        assert finding.suggestion.replacement_code == "b"

    def test_severity_alias_normalization(self):
        finding = FileReviewFinding(severity="H", description="test", diff_side="new", new_line=1, confidence=0.8)
        assert finding.severity == Severity.HIGH

        finding = FileReviewFinding(severity="CRIT", description="test", diff_side="new", new_line=1, confidence=0.8)
        assert finding.severity == Severity.CRITICAL

    def test_model_dump(self):
        finding = FileReviewFinding(severity="low", description="minor", diff_side="new", new_line=10, confidence=0.8)
        data = finding.model_dump()
        assert data["severity"] == "low"
        assert data["new_line"] == 10
        assert data["diff_side"] == "new"

    def test_invalid_severity(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="invalid", description="test", diff_side="new", new_line=1, confidence=0.8)

    def test_legacy_line_inferred_as_new_line(self):
        finding = FileReviewFinding(severity="low", description="d", line=7, confidence=0.8)
        assert finding.diff_side == "new"
        assert finding.new_line == 7
        assert finding.line == 7

    def test_legacy_line_matches_new_line(self):
        finding = FileReviewFinding(
            severity="low",
            description="d",
            line=7,
            new_line=7,
            diff_side="new",
            confidence=0.8,
        )
        assert finding.new_line == 7

    def test_legacy_line_conflicts_with_new_line(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", line=7, new_line=8, diff_side="new", confidence=0.8)

    def test_old_side_finding(self):
        finding = FileReviewFinding(
            severity="low", description="removed line issue", diff_side="old", old_line=3, confidence=0.8
        )
        assert finding.old_line == 3
        assert finding.new_line is None
        assert finding.line is None

    def test_old_side_rejects_new_line(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", diff_side="old", old_line=3, new_line=4, confidence=0.8)

    def test_old_side_missing_coordinate(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", diff_side="old", confidence=0.8)

    def test_new_side_rejects_old_line(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", diff_side="new", old_line=3, new_line=4, confidence=0.8)

    def test_new_side_missing_coordinate(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", diff_side="new", confidence=0.8)

    def test_context_side_requires_both(self):
        finding = FileReviewFinding(
            severity="low", description="d", diff_side="context", old_line=3, new_line=5, confidence=0.8
        )
        assert finding.old_line == 3
        assert finding.new_line == 5

    def test_context_side_missing_coordinate(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", diff_side="context", old_line=3, confidence=0.8)

    def test_diff_side_required_for_new_format(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", new_line=1, confidence=0.8)

    def test_confidence_required(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", diff_side="new", new_line=1)

    def test_confidence_required_for_legacy_line_payload(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", line=1)

    def test_model_validate_preserves_instance_input(self):
        finding = FileReviewFinding(severity="low", description="d", diff_side="new", new_line=1, confidence=0.8)
        validated = FileReviewFinding.model_validate(finding)
        assert validated is finding

    def test_legacy_shape_normalizer_ignores_non_dict_input(self):
        assert FileReviewFinding._normalize_legacy_shape("not-a-dict") == "not-a-dict"

    def test_confidence_low_flag_derived(self):
        finding = FileReviewFinding(severity="low", description="d", diff_side="new", confidence=0.4, new_line=1)
        assert finding.low_confidence is True

    def test_confidence_high_flag_not_set(self):
        finding = FileReviewFinding(severity="low", description="d", diff_side="new", confidence=0.5, new_line=1)
        assert finding.low_confidence is False

    def test_low_confidence_override_ignored(self):
        finding = FileReviewFinding(
            severity="low", description="d", diff_side="new", confidence=0.9, low_confidence=True, new_line=1
        )
        assert finding.low_confidence is False

    def test_low_confidence_rederived_when_confidence_changes(self):
        finding = FileReviewFinding(severity="low", description="d", diff_side="new", confidence=0.9, new_line=1)
        finding.confidence = 0.4
        assert finding.low_confidence is True

    def test_low_confidence_assignment_cannot_drift_from_confidence(self):
        finding = FileReviewFinding(severity="low", description="d", diff_side="new", confidence=0.9, new_line=1)
        finding.low_confidence = True
        assert finding.low_confidence is False

    def test_confidence_out_of_range_rejected(self):
        with pytest.raises(ValidationError):
            FileReviewFinding(severity="low", description="d", diff_side="new", confidence=1.5, new_line=1)
