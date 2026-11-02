"""Tests for ``_bridge_lock_path`` (worktree-key-stable Azure bridge lock path)."""

from unittest.mock import patch

from agentic_devtools.adapters.pull_request_create import (
    _AZURE_BRIDGE_LOCK_FILENAME,
    _bridge_lock_path,
)


def test_lock_path_is_under_repo_root_agdt_directory(tmp_path) -> None:
    with patch("agentic_devtools.adapters.pull_request_create._state_module.get_repo_root", return_value=tmp_path):
        result = _bridge_lock_path()

    assert result == tmp_path / ".agdt" / _AZURE_BRIDGE_LOCK_FILENAME
    assert (tmp_path / ".agdt").is_dir()


def test_lock_path_is_stable_across_state_dir_changes(tmp_path) -> None:
    """The lock path must not move even if `get_state_dir()` would resolve differently."""
    with (
        patch("agentic_devtools.adapters.pull_request_create._state_module.get_repo_root", return_value=tmp_path),
        patch(
            "agentic_devtools.adapters.pull_request_create._state_module.get_state_dir",
            side_effect=[tmp_path / "old", tmp_path / "new"],
        ),
    ):
        first = _bridge_lock_path()
        second = _bridge_lock_path()

    assert first == second


def test_lock_path_falls_back_to_cwd_when_no_repo_root(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    with patch("agentic_devtools.adapters.pull_request_create._state_module.get_repo_root", return_value=None):
        result = _bridge_lock_path()

    assert result == tmp_path / ".agdt" / _AZURE_BRIDGE_LOCK_FILENAME
