"""Tests for _get_issue_comments()."""

import logging
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.evaluator.snapshot_builder import _get_issue_comments


def test_returns_empty_list_without_provider_support() -> None:
    """Returns an empty list when the provider has no issue-comment method."""
    provider = MagicMock()
    del provider.list_issue_comments

    assert _get_issue_comments(provider, 42) == []


def test_returns_provider_comments() -> None:
    """Returns comments fetched from the provider."""
    provider = MagicMock()
    provider.list_issue_comments.return_value = [{"id": 7}]

    assert _get_issue_comments(provider, 42) == [{"id": 7}]
    provider.list_issue_comments.assert_called_once_with(42)


def test_logs_and_returns_empty_list_on_failure(caplog: pytest.LogCaptureFixture) -> None:
    """Logs an optional fetch failure and continues with no comments."""
    provider = MagicMock()
    provider.list_issue_comments.side_effect = RuntimeError("API unavailable")

    with caplog.at_level(logging.WARNING):
        assert _get_issue_comments(provider, 42) == []

    assert "Failed to fetch issue comments for PR #42" in caplog.text
