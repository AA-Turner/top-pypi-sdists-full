"""Tests for the RefreshOutcome dataclass."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.setup.refresh_outcome import RefreshOutcome


class TestRefreshOutcomeValidation:
    """Nullability-rule validation for each status."""

    def test_invalid_status_raises(self) -> None:
        """An unknown status raises ValueError listing the allowed values."""
        with pytest.raises(ValueError, match="Invalid refresh outcome status"):
            RefreshOutcome(status="bogus")

    def test_success_requires_null_reason(self) -> None:
        """success with a non-null reason raises."""
        with pytest.raises(ValueError, match="must have reason=None"):
            RefreshOutcome(status="success", reason="x")

    def test_success_requires_null_error(self) -> None:
        """success with a non-null error raises."""
        with pytest.raises(ValueError, match="must have error=None"):
            RefreshOutcome(status="success", error="x")

    def test_success_valid(self) -> None:
        """success with both fields null is valid."""
        outcome = RefreshOutcome(status="success")
        assert outcome.reason is None
        assert outcome.error is None

    def test_skipped_requires_reason(self) -> None:
        """skipped without a reason raises."""
        with pytest.raises(ValueError, match="requires a non-empty string reason"):
            RefreshOutcome(status="skipped")

    def test_skipped_empty_reason_raises(self) -> None:
        """skipped with an empty-string reason raises."""
        with pytest.raises(ValueError, match="requires a non-empty string reason"):
            RefreshOutcome(status="skipped", reason="")

    def test_skipped_requires_null_error(self) -> None:
        """skipped with a non-null error raises."""
        with pytest.raises(ValueError, match="must have error=None"):
            RefreshOutcome(status="skipped", reason="dry_run", error="x")

    def test_skipped_valid(self) -> None:
        """skipped with a reason and null error is valid."""
        outcome = RefreshOutcome(status="skipped", reason="dry_run")
        assert outcome.reason == "dry_run"
        assert outcome.error is None

    def test_failed_requires_reason(self) -> None:
        """failed without a reason raises."""
        with pytest.raises(ValueError, match="requires a non-empty string reason"):
            RefreshOutcome(status="failed", error="boom")

    def test_failed_requires_error(self) -> None:
        """failed without an error raises."""
        with pytest.raises(ValueError, match="requires a non-empty string error"):
            RefreshOutcome(status="failed", reason="provider_unreachable")

    def test_failed_valid(self) -> None:
        """failed with both reason and error is valid."""
        outcome = RefreshOutcome(status="failed", reason="provider_unreachable", error="boom")
        assert outcome.reason == "provider_unreachable"
        assert outcome.error == "boom"

    def test_skipped_non_string_reason_raises(self) -> None:
        """skipped with a non-string (but truthy) reason raises."""
        with pytest.raises(ValueError, match="requires a non-empty string reason"):
            RefreshOutcome(status="skipped", reason=1)  # type: ignore[arg-type]

    def test_failed_non_string_reason_raises(self) -> None:
        """failed with a non-string (but truthy) reason raises."""
        with pytest.raises(ValueError, match="requires a non-empty string reason"):
            RefreshOutcome(status="failed", reason=1, error="boom")  # type: ignore[arg-type]

    def test_failed_non_string_error_raises(self) -> None:
        """failed with a non-string (but truthy) error raises."""
        with pytest.raises(ValueError, match="requires a non-empty string error"):
            RefreshOutcome(status="failed", reason="provider_unreachable", error=2)  # type: ignore[arg-type]


class TestRefreshOutcomeSerialization:
    """to_dict serialization."""

    def test_to_dict_shape(self) -> None:
        """to_dict returns status/reason/error keys in order."""
        outcome = RefreshOutcome(status="failed", reason="provider_unreachable", error="boom")
        assert outcome.to_dict() == {
            "status": "failed",
            "reason": "provider_unreachable",
            "error": "boom",
        }

    def test_to_dict_success(self) -> None:
        """Success serializes reason/error as null."""
        assert RefreshOutcome(status="success").to_dict() == {
            "status": "success",
            "reason": None,
            "error": None,
        }


class TestRefreshOutcomeFactories:
    """Convenience constructors."""

    def test_success_factory(self) -> None:
        """success() builds a success outcome."""
        outcome = RefreshOutcome.success()
        assert outcome.status == "success"
        assert outcome.reason is None
        assert outcome.error is None

    def test_skipped_factory(self) -> None:
        """skipped() builds a skipped outcome with the given reason."""
        outcome = RefreshOutcome.skipped("missing_config")
        assert outcome.status == "skipped"
        assert outcome.reason == "missing_config"
        assert outcome.error is None

    def test_failed_factory(self) -> None:
        """failed() builds a failed outcome with reason and error."""
        outcome = RefreshOutcome.failed("provider_unreachable", "boom")
        assert outcome.status == "failed"
        assert outcome.reason == "provider_unreachable"
        assert outcome.error == "boom"
