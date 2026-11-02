"""Tests for _browser_profile_dir."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.github import browser_apply_autofix


class TestBrowserProfileDir:
    """Tests for selecting the persistent browser profile directory."""

    def test_uses_explicit_profile_dir(self, tmp_path) -> None:
        explicit = tmp_path / "profile"

        assert browser_apply_autofix._browser_profile_dir(explicit) == explicit

    def test_uses_environment_override(self, tmp_path) -> None:
        configured = tmp_path / "configured"

        with patch.dict("os.environ", {"AGDT_BROWSER_PROFILE_DIR": str(configured)}):
            assert browser_apply_autofix._browser_profile_dir() == configured

    def test_uses_default_profile_dir_when_unconfigured(self, tmp_path) -> None:
        with (
            patch.dict("os.environ", {}, clear=True),
            patch.object(Path, "home", return_value=tmp_path),
        ):
            result = browser_apply_autofix._browser_profile_dir()
            default = browser_apply_autofix._default_browser_profile_dir()

        assert result == default
        assert isinstance(result, Path)
