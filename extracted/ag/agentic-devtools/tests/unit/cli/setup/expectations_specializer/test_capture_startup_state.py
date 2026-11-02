"""Tests for ``capture_startup_state``."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.setup.expectations_specializer import (
    SPECIALIZED_OUTPUT_FILENAME,
    capture_startup_state,
)


class TestCaptureStartupState:
    """Verify startup-state capture behavior."""

    def test_binds_state_dir_to_fingerprint(self, tmp_path: Path) -> None:
        """Captures the startup fingerprint alongside the exact state directory it belongs to."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("existing", encoding="utf-8")

        result = capture_startup_state(tmp_path)

        assert result.state_dir == tmp_path
        assert result.fingerprint is not None
        assert isinstance(result.fingerprint, tuple)
