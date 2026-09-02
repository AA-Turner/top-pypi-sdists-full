"""Tests for is_git_hooks_management_enabled."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.cli.setup.git_hooks_policy import (
    NON_BOOLEAN_WARNING_PREFIX,
    is_git_hooks_management_enabled,
)


def _write_config(git_root: Path, payload: object) -> None:
    config_path = git_root / ".agdt" / "config" / "project.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(payload), encoding="utf-8")


class TestIsGitHooksManagementEnabled:
    """Tests for is_git_hooks_management_enabled."""

    def test_returns_true_when_config_file_absent(self, tmp_path: Path) -> None:
        """No project.json → enabled (default)."""
        assert is_git_hooks_management_enabled(tmp_path) is True

    def test_returns_true_when_key_absent(self, tmp_path: Path) -> None:
        """project.json without the key → enabled (default)."""
        _write_config(tmp_path, {"other": "value"})
        assert is_git_hooks_management_enabled(tmp_path) is True

    def test_returns_true_when_key_is_null(self, tmp_path: Path) -> None:
        """Explicit JSON null → enabled (default)."""
        _write_config(tmp_path, {"manage_git_hooks": None})
        assert is_git_hooks_management_enabled(tmp_path) is True

    def test_returns_true_when_key_is_true(self, tmp_path: Path) -> None:
        """Explicit true → enabled."""
        _write_config(tmp_path, {"manage_git_hooks": True})
        assert is_git_hooks_management_enabled(tmp_path) is True

    def test_returns_false_when_key_is_false(self, tmp_path: Path) -> None:
        """Explicit false → disabled."""
        _write_config(tmp_path, {"manage_git_hooks": False})
        assert is_git_hooks_management_enabled(tmp_path) is False

    def test_non_boolean_warns_and_returns_true(self, tmp_path: Path, capsys) -> None:
        """A non-boolean value warns on stderr and is treated as enabled."""
        _write_config(tmp_path, {"manage_git_hooks": "false"})

        assert is_git_hooks_management_enabled(tmp_path) is True

        captured = capsys.readouterr()
        assert NON_BOOLEAN_WARNING_PREFIX in captured.err
        assert "'false'" in captured.err
        assert captured.out == ""

    def test_returns_true_when_json_is_malformed(self, tmp_path: Path) -> None:
        """Malformed JSON → enabled (default), no exception."""
        config_path = tmp_path / ".agdt" / "config" / "project.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("{not json", encoding="utf-8")

        assert is_git_hooks_management_enabled(tmp_path) is True

    def test_returns_true_when_json_root_is_not_a_dict(self, tmp_path: Path) -> None:
        """Non-object JSON root → enabled (default)."""
        _write_config(tmp_path, ["manage_git_hooks"])
        assert is_git_hooks_management_enabled(tmp_path) is True
