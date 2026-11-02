"""Tests for resolve_preset_dir() (FR-004)."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.issue_template import validate_templates as vt
from agentic_devtools.cli.issue_template._repo_paths import _PRESET_DIR_RELATIVE
from agentic_devtools.cli.issue_template.validate_templates import resolve_preset_dir


class TestResolvePresetDir:
    """Tests for preset directory resolution priority."""

    def test_explicit_arg_takes_precedence(self) -> None:
        """An explicit --preset-dir argument is returned as a Path."""
        assert resolve_preset_dir("/some/dir") == Path("/some/dir")

    def test_auto_discovery_from_repo_root(self, monkeypatch) -> None:
        """When no arg is given, resolve from repo root + relative preset path."""
        monkeypatch.setattr(vt, "_find_repo_root", lambda: Path("/repo"))
        assert resolve_preset_dir(None) == Path("/repo") / _PRESET_DIR_RELATIVE

    def test_returns_none_when_no_repo_root(self, monkeypatch) -> None:
        """When no arg and no repo root is found, return None."""
        monkeypatch.setattr(vt, "_find_repo_root", lambda: None)
        assert resolve_preset_dir(None) is None
