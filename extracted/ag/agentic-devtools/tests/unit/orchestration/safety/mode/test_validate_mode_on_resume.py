"""Tests for validate_mode_on_resume() — FR-001 resume mismatch rejection."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.safety.mode import ExecutionMode, validate_mode_on_resume


class TestValidateModeOnResume:
    """Tests for resume mode validation."""

    def test_none_persisted_returns_resolved(self) -> None:
        result = validate_mode_on_resume(None, ExecutionMode.dry_run)
        assert result == ExecutionMode.dry_run

    def test_same_mode_passes(self) -> None:
        result = validate_mode_on_resume("dry_run", ExecutionMode.dry_run)
        assert result == ExecutionMode.dry_run

    def test_mismatch_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="mode mismatch on resume"):
            validate_mode_on_resume("live", ExecutionMode.dry_run)

    def test_mismatch_with_force_override_succeeds(self) -> None:
        result = validate_mode_on_resume("live", ExecutionMode.dry_run, force_override=True)
        assert result == ExecutionMode.dry_run

    def test_invalid_persisted_mode_treated_as_first_run(self) -> None:
        result = validate_mode_on_resume("garbage", ExecutionMode.restricted)
        assert result == ExecutionMode.restricted

    def test_live_to_restricted_mismatch(self) -> None:
        with pytest.raises(ValueError):
            validate_mode_on_resume("live", ExecutionMode.restricted)

    def test_mismatch_error_references_python_api(self) -> None:
        """Mismatch error message must reference the Python API, not a CLI flag."""
        with pytest.raises(ValueError) as exc_info:
            validate_mode_on_resume("live", ExecutionMode.dry_run)
        assert "force_override=True" in str(exc_info.value)
        assert "--force-mode-override" not in str(exc_info.value)
