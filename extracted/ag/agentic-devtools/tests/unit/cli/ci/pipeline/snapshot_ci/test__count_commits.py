"""Tests for commit-count metadata helpers."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_ci import _count_commits


def test_returns_provider_count_as_integer() -> None:
    provider = MagicMock()
    provider.count_commits_above_merge_base.return_value = "3"

    assert _count_commits(provider, base_branch="main", head_sha="head") == 3


def test_defaults_to_one_when_provider_does_not_support_counting() -> None:
    provider = MagicMock()
    provider.count_commits_above_merge_base = None

    assert _count_commits(provider, base_branch="main", head_sha="head") == 1


def test_propagates_provider_errors() -> None:
    provider = MagicMock()
    provider.count_commits_above_merge_base.side_effect = RuntimeError("git unavailable")

    with pytest.raises(RuntimeError, match="git unavailable"):
        _count_commits(provider, base_branch="main", head_sha="head")
