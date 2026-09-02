"""Tests for ``cleanup_specialized_output``."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.expectations_specializer import (
    SPECIALIZED_OUTPUT_FILENAME,
    _StartupFingerprintError,
    _StartupFingerprintState,
    cleanup_specialized_output,
)


class TestCleanupSpecializedOutput:
    """Verify startup-owned specialized-output cleanup behavior."""

    def test_removes_matching_output(self, tmp_path: Path) -> None:
        """A matching startup-owned artifact is removed under the shared cleanup transaction."""
        output = tmp_path / "setup-expectations-specialized.md"
        output.write_text("stale", encoding="utf-8")

        result = cleanup_specialized_output(tmp_path, status="skipped", reason="skip")

        assert result.status == "skipped"
        assert not output.exists()

    def test_keeps_changed_output(self, tmp_path: Path) -> None:
        """A changed artifact is preserved so a later failing run cannot delete fresh output."""
        output = tmp_path / "setup-expectations-specialized.md"
        output.write_text("fresh", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.setup.expectations_specializer._output_fingerprint",
            side_effect=[(1, 2, 3), (4, 5, 6)],
        ):
            result = cleanup_specialized_output(tmp_path, status="skipped", reason="skip")

        assert result.status == "skipped"
        assert output.exists()

    def test_lock_failure_returns_error_result(self, tmp_path: Path) -> None:
        """An ``OSError`` while acquiring the lock returns an error result."""
        output = tmp_path / "setup-expectations-specialized.md"
        output.write_text("STALE CONTENT", encoding="utf-8")

        with patch("agentic_devtools.file_locking.locked_file", side_effect=OSError("lock failed")):
            result = cleanup_specialized_output(tmp_path, status="skipped", reason="skip")

        assert result.status == "error"
        assert result.reason is not None
        assert "lock failed" in result.reason

    def test_fingerprint_oserror_returns_error_result(self, tmp_path: Path) -> None:
        """An ``OSError`` from ``_output_fingerprint`` at startup returns an error result."""
        with patch(
            "agentic_devtools.cli.setup.expectations_specializer._output_fingerprint",
            side_effect=OSError("permission denied"),
        ):
            result = cleanup_specialized_output(tmp_path, status="skipped", reason="skip")

        assert result.status == "error"
        assert result.reason is not None
        assert "permission denied" in result.reason

    def test_startup_fingerprint_error_marker_returns_error_result(self, tmp_path: Path) -> None:
        """A startup inspection failure marker is surfaced as an error result."""
        result = cleanup_specialized_output(
            tmp_path,
            status="skipped",
            reason="skip",
            startup_fingerprint=_StartupFingerprintError(error=OSError("permission denied")),
        )

        assert result.status == "error"
        assert result.reason is not None
        assert "permission denied" in result.reason

    def test_provided_startup_fingerprint_is_used_directly(self, tmp_path: Path) -> None:
        """When ``startup_fingerprint`` is supplied, it is used instead of computing at cleanup time.

        The file matches the provided fingerprint so it is removed; if the fingerprint were
        re-computed at cleanup time the test would still pass, but we verify the
        ``_output_fingerprint`` helper is NOT called a second time so only the pre-supplied
        fingerprint governs the guard decision.
        """
        output = tmp_path / "setup-expectations-specialized.md"
        output.write_text("stale", encoding="utf-8")
        stat = output.stat()
        startup_fp = (stat.st_ino, stat.st_size, stat.st_mtime_ns)

        call_count = 0

        original = __import__(
            "agentic_devtools.cli.setup.expectations_specializer",
            fromlist=["_output_fingerprint"],
        )._output_fingerprint

        def tracking_fingerprint(path: object) -> object:
            nonlocal call_count
            call_count += 1
            return original(path)  # type: ignore[arg-type]

        with patch(
            "agentic_devtools.cli.setup.expectations_specializer._output_fingerprint",
            side_effect=tracking_fingerprint,
        ):
            result = cleanup_specialized_output(
                tmp_path,
                status="skipped",
                reason="skip",
                startup_fingerprint=startup_fp,
            )

        assert result.status == "skipped"
        assert not output.exists()
        # _output_fingerprint was called once (for the re-check inside the lock),
        # not twice (startup capture is skipped when startup_fingerprint is provided).
        assert call_count == 1

    def test_startup_snapshot_binds_cleanup_to_original_state_dir(self, tmp_path: Path) -> None:
        """A startup snapshot binds cleanup to the original state directory."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)
        snapshot = _StartupFingerprintState(state_dir=tmp_path, fingerprint=fingerprint)

        result = cleanup_specialized_output(tmp_path / "other", reason="stale cleanup", startup_fingerprint=snapshot)

        assert result.status == "skipped"
        assert not output.exists()
