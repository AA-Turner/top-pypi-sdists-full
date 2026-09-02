"""Tests for resolve_phase_0_enabled in speckit/phase0/helpers.py (FR-001)."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.cli.speckit.phase0.helpers import resolve_phase_0_enabled


def _write_config(repo_path: Path, phase_0: object) -> None:
    """Write a minimal ``.github/agdt-config.json`` with the given phase_0."""
    github_dir = repo_path / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)
    config = {"platform": {"phase_0": phase_0}}
    (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")


class TestResolvePhase0Enabled:
    """Tests for the resolve_phase_0_enabled function."""

    def test_enabled_true(self, tmp_path: Path) -> None:
        _write_config(tmp_path, {"enabled": True})
        assert resolve_phase_0_enabled(str(tmp_path)) is True

    def test_enabled_false(self, tmp_path: Path) -> None:
        _write_config(tmp_path, {"enabled": False})
        assert resolve_phase_0_enabled(str(tmp_path)) is False

    def test_absent_config_defaults_to_false(self, tmp_path: Path) -> None:
        assert resolve_phase_0_enabled(str(tmp_path)) is False

    def test_missing_enabled_key_defaults_to_false(self, tmp_path: Path) -> None:
        _write_config(tmp_path, {})
        assert resolve_phase_0_enabled(str(tmp_path)) is False
