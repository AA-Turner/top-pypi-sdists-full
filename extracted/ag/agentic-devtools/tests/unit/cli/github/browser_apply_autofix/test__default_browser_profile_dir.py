"""Tests for _default_browser_profile_dir."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.github import browser_apply_autofix


class TestDefaultBrowserProfileDir:
    """Tests for the platform-specific default browser profile directory."""

    def test_uses_local_app_data_on_windows_when_available(self, tmp_path) -> None:
        with (
            patch.object(browser_apply_autofix.sys, "platform", "win32"),
            patch.dict("os.environ", {"LOCALAPPDATA": str(tmp_path)}),
        ):
            result = browser_apply_autofix._default_browser_profile_dir()

        assert result == tmp_path / "ai-pr-loop-supervision" / "browser-profile"

    def test_uses_windows_home_fallback_when_local_app_data_is_unset(self, tmp_path) -> None:
        env = {key: value for key, value in os.environ.items() if key != "LOCALAPPDATA"}
        with (
            patch.object(browser_apply_autofix.sys, "platform", "win32"),
            patch.dict("os.environ", env, clear=True),
            patch.object(Path, "home", return_value=tmp_path),
        ):
            result = browser_apply_autofix._default_browser_profile_dir()

        assert result == tmp_path / "AppData" / "Local" / "ai-pr-loop-supervision" / "browser-profile"

    def test_ignores_inherited_local_app_data_on_posix(self, tmp_path) -> None:
        # A POSIX process that inherited a LOCALAPPDATA value (e.g. from a
        # copied Windows environment) must still use the POSIX layout.
        with (
            patch.object(browser_apply_autofix.sys, "platform", "linux"),
            patch.dict("os.environ", {"LOCALAPPDATA": "/should/be/ignored"}),
            patch.object(Path, "home", return_value=tmp_path),
        ):
            result = browser_apply_autofix._default_browser_profile_dir()

        assert result == tmp_path / ".local" / "share" / "ai-pr-loop-supervision" / "browser-profile"

    def test_uses_home_data_directory_when_not_windows(self, tmp_path) -> None:
        env = {key: value for key, value in os.environ.items() if key != "LOCALAPPDATA"}
        with (
            patch.object(browser_apply_autofix.sys, "platform", "linux"),
            patch.dict("os.environ", env, clear=True),
            patch.object(Path, "home", return_value=tmp_path),
        ):
            result = browser_apply_autofix._default_browser_profile_dir()

        assert result == tmp_path / ".local" / "share" / "ai-pr-loop-supervision" / "browser-profile"
