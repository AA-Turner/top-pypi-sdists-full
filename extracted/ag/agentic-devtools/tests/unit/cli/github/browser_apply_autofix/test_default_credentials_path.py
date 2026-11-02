"""Tests for _default_credentials_path."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.github import browser_apply_autofix


class TestDefaultCredentialsPath:
    """Tests for _default_credentials_path."""

    def test_points_to_user_credentials_json_next_to_module(self) -> None:
        path = browser_apply_autofix._default_credentials_path()
        assert isinstance(path, Path)
        assert path.name == "user_credentials.json"
        assert path.parent == Path(browser_apply_autofix.__file__).parent
