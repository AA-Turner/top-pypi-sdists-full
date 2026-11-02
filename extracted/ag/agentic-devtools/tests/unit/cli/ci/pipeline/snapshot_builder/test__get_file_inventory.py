"""Tests for _get_file_inventory."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_builder import _get_file_inventory


def test_prefers_inventory_pinned_to_head() -> None:
    """An overridden diff inventory is queried with the requested HEAD."""
    provider = MagicMock()
    provider.compute_diff_files = MagicMock(return_value=["a.py"])

    result = _get_file_inventory(provider, 7, "main", "head", {"base_sha": "base"})

    assert result == ["a.py"]
    provider.compute_diff_files.assert_called_once_with(base_branch="main", sha="head", base_sha="base")
    provider.list_pr_files.assert_not_called()


def test_unsupported_pinned_inventory_falls_back_to_live_pr_files() -> None:
    """A provider without pinned inventory support uses its PR file listing."""
    provider = MagicMock()
    provider.compute_diff_files = None
    provider.list_pr_files.return_value = ["fallback.py"]

    assert _get_file_inventory(provider, 7, "main", "head", {}) == ["fallback.py"]


def test_missing_pinned_inventory_fails_closed() -> None:
    """A supported provider returning no exact-HEAD inventory raises."""
    provider = MagicMock()
    provider.compute_diff_files = MagicMock(return_value=None)

    with pytest.raises(RuntimeError, match="exact-HEAD file inventory unavailable"):
        _get_file_inventory(provider, 7, "main", "head", {})


def test_pinned_inventory_errors_are_not_hidden_by_fallback() -> None:
    """An exact-HEAD query failure propagates instead of mixing snapshots."""
    provider = MagicMock()
    provider.compute_diff_files = MagicMock(side_effect=RuntimeError("lookup failed"))

    with pytest.raises(RuntimeError, match="lookup failed"):
        _get_file_inventory(provider, 7, "main", "head", {})
