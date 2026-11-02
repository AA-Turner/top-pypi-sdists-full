"""Tests for _resolve_npm_enabled."""

import argparse
from pathlib import Path

from agentic_devtools.cli.setup import commands


class TestResolveNpmEnabled:
    """Tests for _resolve_npm_enabled."""

    def test_npm_flag_returns_true_regardless_of_footprint(self, tmp_path: Path) -> None:
        """--npm flag forces True even when no npm footprint exists."""
        args = argparse.Namespace(npm=True, no_npm=False)
        assert commands._resolve_npm_enabled(args, tmp_path) is True

    def test_no_npm_flag_returns_false_regardless_of_footprint(self, tmp_path: Path) -> None:
        """--no-npm flag forces False even when npm footprint exists."""
        (tmp_path / "package.json").write_text("{}", encoding="utf-8")
        args = argparse.Namespace(npm=False, no_npm=True)
        assert commands._resolve_npm_enabled(args, tmp_path) is False

    def test_neither_flag_delegates_to_detect_npm_footprint_true(self, tmp_path: Path) -> None:
        """Without flags, delegates to detect_npm_footprint (returns True when present)."""
        (tmp_path / "package.json").write_text("{}", encoding="utf-8")
        args = argparse.Namespace(npm=False, no_npm=False)
        assert commands._resolve_npm_enabled(args, tmp_path) is True

    def test_neither_flag_delegates_to_detect_npm_footprint_false(self, tmp_path: Path) -> None:
        """Without flags, delegates to detect_npm_footprint (returns False when absent)."""
        args = argparse.Namespace(npm=False, no_npm=False)
        assert commands._resolve_npm_enabled(args, tmp_path) is False

    def test_uses_directory_parameter_for_detection(self, tmp_path: Path) -> None:
        """Uses the provided directory for footprint detection, not CWD."""
        # Create indicator in a specific directory, not CWD
        subdir = tmp_path / "myrepo"
        subdir.mkdir()
        (subdir / "yarn.lock").write_text("", encoding="utf-8")
        args = argparse.Namespace(npm=False, no_npm=False)
        assert commands._resolve_npm_enabled(args, subdir) is True
        # The parent should not detect anything
        assert commands._resolve_npm_enabled(args, tmp_path) is False

    def test_handles_missing_npm_attr_gracefully(self, tmp_path: Path) -> None:
        """Handles args without npm/no_npm attributes (getattr defaults to False)."""
        args = argparse.Namespace()
        (tmp_path / "package.json").write_text("{}", encoding="utf-8")
        assert commands._resolve_npm_enabled(args, tmp_path) is True
