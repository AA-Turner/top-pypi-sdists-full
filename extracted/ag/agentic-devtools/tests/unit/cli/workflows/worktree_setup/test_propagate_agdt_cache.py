"""Tests for propagate_agdt_cache."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.workflows.worktree_setup import propagate_agdt_cache


@patch("agentic_devtools.cli.workflows.worktree_setup._propagate_agdt_cache")
def test_propagate_agdt_cache_delegates_to_private_impl(mock_impl, tmp_path):
    propagate_agdt_cache(str(tmp_path), worktree_key="42")

    mock_impl.assert_called_once_with(str(tmp_path), worktree_key="42", strict=True)


@patch("agentic_devtools.cli.workflows.worktree_setup._propagate_agdt_cache")
def test_propagate_agdt_cache_passes_none_worktree_key(mock_impl, tmp_path):
    propagate_agdt_cache(str(tmp_path))

    mock_impl.assert_called_once_with(str(tmp_path), worktree_key=None, strict=True)


@patch(
    "agentic_devtools.cli.workflows.worktree_setup._propagate_agdt_cache",
    side_effect=OSError("disk full"),
)
def test_propagate_agdt_cache_raises_on_oserror(mock_impl, tmp_path):
    """OSError from the private impl propagates through the public API."""
    with pytest.raises(OSError, match="disk full"):
        propagate_agdt_cache(str(tmp_path))


@patch(
    "agentic_devtools.cli.workflows.worktree_setup._propagate_agdt_cache",
    side_effect=ValueError("bad value"),
)
def test_propagate_agdt_cache_raises_on_valueerror(mock_impl, tmp_path):
    """ValueError from the private impl propagates through the public API."""
    with pytest.raises(ValueError, match="bad value"):
        propagate_agdt_cache(str(tmp_path))
