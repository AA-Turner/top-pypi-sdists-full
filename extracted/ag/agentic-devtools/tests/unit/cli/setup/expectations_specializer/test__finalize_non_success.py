"""Tests for ``_finalize_non_success``."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.expectations_specializer import (
    SPECIALIZED_OUTPUT_FILENAME,
    _finalize_non_success,
)


class TestFinalizeNonSuccess:
    """Verify stale-output cleanup behavior for non-success paths."""

    def test_lock_acquisition_failure_is_surfaced_as_error(self, tmp_path: Path) -> None:
        """Lock failures during stale-output cleanup are surfaced as errors."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)

        with patch("agentic_devtools.file_locking.locked_file", side_effect=OSError("lock failed")):
            result = _finalize_non_success(output, fingerprint, status="error", reason="cleanup failed")

        assert result.status == "error"
        assert result.reason is not None
        assert "failed to acquire lock" in result.reason
