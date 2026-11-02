"""Tests for _profile_lock_path."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.github.browser_apply_autofix import _profile_lock_path


class TestProfileLockPath:
    """Tests for the sibling lock-file path helper."""

    def test_returns_sibling_lock_file(self, tmp_path) -> None:
        profile_dir = tmp_path / "browser-profile"

        result = _profile_lock_path(profile_dir)

        assert result == tmp_path / "browser-profile.lock"
        assert isinstance(result, Path)
