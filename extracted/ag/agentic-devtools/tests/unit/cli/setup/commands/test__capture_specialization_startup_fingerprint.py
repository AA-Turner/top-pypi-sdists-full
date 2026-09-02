"""Tests for _capture_specialization_startup_fingerprint."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.expectations_specializer import (
    _StartupFingerprintError,
    _StartupFingerprintState,
)


class TestCaptureSpecializationStartupFingerprint:
    """Verify startup fingerprint capture semantics for setup specialization."""

    def test_returns_none_without_resolving_state_dir_on_dry_run(self) -> None:
        """Dry-run returns None and skips all startup artifact probing."""
        with patch("agentic_devtools.state.get_state_dir", side_effect=AssertionError("should not be called")):
            assert commands._capture_specialization_startup_fingerprint(dry_run=True) is None

    def test_returns_error_marker_when_state_dir_resolution_fails(self) -> None:
        """State-dir resolution failures are preserved as startup error markers."""
        with patch("agentic_devtools.state.get_state_dir", side_effect=OSError("state unavailable")):
            result = commands._capture_specialization_startup_fingerprint(dry_run=False)

        assert isinstance(result, _StartupFingerprintError)
        assert "state unavailable" in str(result.error)

    def test_delegates_to_capture_helper_for_live_runs(self, tmp_path: Path) -> None:
        """Live runs resolve the state dir (create=False) and keep it attached to the startup fingerprint."""
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path) as mock_get,
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.capture_startup_fingerprint",
                return_value=(1, 2, 3),
            ) as mock_capture,
        ):
            result = commands._capture_specialization_startup_fingerprint(dry_run=False)

        mock_get.assert_called_once_with(create=False)
        assert isinstance(result, _StartupFingerprintState)
        assert result.state_dir == tmp_path
        assert result.fingerprint == (1, 2, 3)
        mock_capture.assert_called_once_with(tmp_path)
