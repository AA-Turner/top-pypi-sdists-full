"""Tests for _cleanup_stale_specialization_artifact."""

from unittest.mock import patch

from agentic_devtools.cli.setup import commands
from agentic_devtools.cli.setup.expectations_specializer import SpecializationResult


class TestCleanupStaleSpecializationArtifact:
    """Verify non-fatal early-exit cleanup behaviour."""

    def test_no_warning_when_cleanup_succeeds(self, capsys, tmp_path) -> None:
        """No stderr output when cleanup returns a non-error status."""
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.cleanup_specialized_output",
                return_value=SpecializationResult(status="skipped", reason="no artifact"),
            ),
        ):
            commands._cleanup_stale_specialization_artifact("test reason", startup_fingerprint=None)

        assert capsys.readouterr().err == ""

    def test_warning_emitted_when_cleanup_returns_error(self, capsys, tmp_path) -> None:
        """A stderr warning is emitted when cleanup_specialized_output returns an error result."""
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.cleanup_specialized_output",
                return_value=SpecializationResult(status="error", reason="lock failed"),
            ),
        ):
            commands._cleanup_stale_specialization_artifact("test reason", startup_fingerprint=None)

        err = capsys.readouterr().err
        assert "Failed to clean up stale setup-expectations-specialized.md" in err
        assert "lock failed" in err

    def test_warning_emitted_on_unexpected_exception(self, capsys) -> None:
        """A stderr warning is emitted when an unexpected exception is raised."""
        with patch(
            "agentic_devtools.state.get_state_dir",
            side_effect=RuntimeError("state unavailable"),
        ):
            commands._cleanup_stale_specialization_artifact("test reason", startup_fingerprint=None)

        err = capsys.readouterr().err
        assert "Failed to clean up stale setup-expectations-specialized.md" in err
        assert "state unavailable" in err
