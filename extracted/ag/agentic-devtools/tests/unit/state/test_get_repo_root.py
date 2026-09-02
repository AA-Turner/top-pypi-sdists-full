"""Tests for agentic_devtools.state.get_repo_root."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools import state


def test_get_repo_root_delegates_to_get_git_repo_root(tmp_path):
    """get_repo_root delegates to _get_git_repo_root and returns its result."""
    with patch.object(state, "_get_git_repo_root", return_value=tmp_path) as mock_inner:
        result = state.get_repo_root()

    assert result == tmp_path
    mock_inner.assert_called_once_with()


def test_get_repo_root_returns_none_when_not_in_repo():
    """get_repo_root returns None when _get_git_repo_root returns None."""
    with patch.object(state, "_get_git_repo_root", return_value=None):
        result = state.get_repo_root()

    assert result is None


def test_get_repo_root_returns_path_type(tmp_path):
    """get_repo_root return type is Path when a repo root is found."""
    with patch.object(state, "_get_git_repo_root", return_value=tmp_path):
        result = state.get_repo_root()

    assert isinstance(result, Path)
