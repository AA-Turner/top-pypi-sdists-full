"""Tests for PerFileReviewError model."""

import pytest
from pydantic import ValidationError

from agentic_devtools.orchestration.schemas.review.per_file_error import PerFileReviewError


class TestPerFileReviewError:
    """Tests for PerFileReviewError construction and retryable mapping."""

    def test_construction_minimal(self):
        err = PerFileReviewError(file_path="f.py", error_kind="unknown")
        assert err.file_path == "f.py"
        assert err.error_kind == "unknown"
        assert err.attempt_count == 0
        assert err.model_id == ""

    @pytest.mark.parametrize(
        "kind",
        ["malformed_output", "rate_limit", "transient_provider"],
    )
    def test_retryable_kinds(self, kind):
        err = PerFileReviewError(file_path="f.py", error_kind=kind)
        assert err.retryable is True

    @pytest.mark.parametrize(
        "kind",
        ["unsupported_configuration", "unknown"],
    )
    def test_non_retryable_kinds(self, kind):
        err = PerFileReviewError(file_path="f.py", error_kind=kind)
        assert err.retryable is False

    def test_retryable_override_ignored(self):
        err = PerFileReviewError(file_path="f.py", error_kind="unknown", retryable=True)
        assert err.retryable is False

    def test_retryable_override_forced_true(self):
        err = PerFileReviewError(file_path="f.py", error_kind="rate_limit", retryable=False)
        assert err.retryable is True

    def test_retryable_rederived_when_error_kind_changes(self):
        err = PerFileReviewError(file_path="f.py", error_kind="unknown")
        err.error_kind = "rate_limit"
        assert err.retryable is True

    def test_retryable_assignment_cannot_drift_from_error_kind(self):
        err = PerFileReviewError(file_path="f.py", error_kind="unknown")
        err.retryable = True
        assert err.retryable is False

    def test_invalid_error_kind_rejected(self):
        with pytest.raises(ValidationError):
            PerFileReviewError(file_path="f.py", error_kind="boom")

    def test_negative_attempt_count_rejected(self):
        with pytest.raises(ValidationError):
            PerFileReviewError(file_path="f.py", error_kind="unknown", attempt_count=-1)

    def test_round_trip(self):
        original = PerFileReviewError(
            file_path="f.py",
            request_id="r1",
            chunk_id="c1",
            model_id="gpt-4o",
            attempt_count=3,
            error_kind="rate_limit",
            message="throttled",
        )
        restored = PerFileReviewError.model_validate_json(original.model_dump_json())
        assert original == restored
        assert restored.retryable is True

    def test_exported_from_review_package(self):
        from agentic_devtools.orchestration.schemas.review import (
            PerFileReviewError as Exported,
        )

        assert Exported is PerFileReviewError

    def test_exported_from_top_level_package(self):
        from agentic_devtools.orchestration.schemas import (
            PerFileReviewError as Exported,
        )

        assert Exported is PerFileReviewError
