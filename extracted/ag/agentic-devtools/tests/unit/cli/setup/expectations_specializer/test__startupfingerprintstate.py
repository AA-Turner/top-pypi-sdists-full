"""Tests for ``_StartupFingerprintState``."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.setup.expectations_specializer import (
    SPECIALIZED_OUTPUT_FILENAME,
    _StartupFingerprintState,
)


class TestStartupFingerprintState:
    """Verify startup-fingerprint state dataclass behavior."""

    def test_binds_state_dir_and_fingerprint(self, tmp_path: Path) -> None:
        """A startup snapshot stays bound to the state directory it was captured from."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)

        snapshot = _StartupFingerprintState(state_dir=tmp_path, fingerprint=fingerprint)

        assert snapshot.state_dir == tmp_path
        assert snapshot.fingerprint == fingerprint
