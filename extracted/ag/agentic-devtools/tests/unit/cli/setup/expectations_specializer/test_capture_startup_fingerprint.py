"""Tests for ``capture_startup_fingerprint``."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.expectations_specializer import (
    SPECIALIZED_OUTPUT_FILENAME,
    _StartupFingerprintError,
    capture_startup_fingerprint,
)


class TestCaptureStartupFingerprint:
    """Verify startup fingerprint capture behavior."""

    def test_returns_none_when_file_absent(self, tmp_path: Path) -> None:
        """Returns ``None`` when the specialized output does not yet exist."""
        result = capture_startup_fingerprint(tmp_path)
        assert result is None

    def test_returns_fingerprint_when_file_present(self, tmp_path: Path) -> None:
        """Returns a non-None tuple fingerprint when the output file exists."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("existing", encoding="utf-8")

        result = capture_startup_fingerprint(tmp_path)

        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_returns_error_marker_on_oserror(self, tmp_path: Path) -> None:
        """Returns an error marker when startup fingerprint inspection fails."""
        with patch(
            "agentic_devtools.cli.setup.expectations_specializer._output_fingerprint",
            side_effect=OSError("permission denied"),
        ):
            result = capture_startup_fingerprint(tmp_path)

        assert isinstance(result, _StartupFingerprintError)
        assert "permission denied" in str(result.error)

    def test_stat_oserror_is_wrapped_in_error_marker(self, tmp_path: Path) -> None:
        """An ``OSError`` from ``Path.stat`` is wrapped in a structured error marker."""
        with patch.object(Path, "stat", side_effect=OSError("permission denied")):
            result = capture_startup_fingerprint(tmp_path)

        assert isinstance(result, _StartupFingerprintError)
        assert "permission denied" in str(result.error)
