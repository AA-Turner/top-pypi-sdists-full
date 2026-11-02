"""Tests for resolving the output of a conflict repair."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.runner import _find_conflict_repair_output
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


@pytest.mark.parametrize(
    ("commits", "expected"),
    [
        ([{"sha": "P"}, {"sha": "R", "parents": [{"sha": "P"}]}, {"sha": "H"}], "R"),
        ([{"sha": "P"}, {"sha": "F"}, {"sha": "R", "parents": [{"sha": "P"}]}, {"sha": "H"}], "R"),
        ([{"sha": "P"}, {"sha": "R"}, {"sha": "H"}], "R"),
        ([{"sha": "P"}, {"sha": "H", "parents": [{"sha": "P"}]}], "H"),
    ],
)
def test_selects_repair_output(commits, expected):
    provider = MagicMock()
    provider.list_pr_commits.return_value = commits
    assert _find_conflict_repair_output(provider, 1, "P", "H") == expected
    provider.list_pr_commits.assert_called_once_with(1)


@pytest.mark.parametrize(
    "commits",
    [
        None,
        [],
        [{"sha": "H"}],
        [{"sha": "P"}],
        [{"sha": "H"}, {"sha": "P"}],
        [None],
        [{"sha": None}],
        [{"sha": ""}],
        [{"sha": "P", "parents": None}],
        [{"sha": "P", "parents": [None]}],
        [{"sha": "P", "parents": [{"sha": None}]}],
    ],
)
def test_unavailable_or_unrelated_history_fails_closed(commits, caplog):
    provider = MagicMock()
    provider.list_pr_commits.return_value = commits
    assert _find_conflict_repair_output(provider, 1, "P", "H") == ""
    assert "conflict-repair output unavailable" in caplog.text


@pytest.mark.parametrize("error", [RuntimeError("history failed"), ProviderRateLimitError(is_rate_limit=False)])
def test_commit_read_failure_is_logged(error, caplog):
    provider = MagicMock()
    provider.list_pr_commits.side_effect = error
    assert _find_conflict_repair_output(provider, 1, "P", "H") == ""
    assert str(error) in caplog.text


def test_rate_limit_propagates():
    provider = MagicMock()
    error = ProviderRateLimitError(is_rate_limit=True)
    provider.list_pr_commits.side_effect = error
    with pytest.raises(ProviderRateLimitError):
        _find_conflict_repair_output(provider, 1, "P", "H")
