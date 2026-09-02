"""Tests for count_prior_executable_posted_findings in the defer_suppressed module."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import ReviewCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.defer_suppressed import (
    count_prior_executable_posted_findings,
)


def _comment(
    *,
    path: str,
    is_suppressed: bool = False,
    author_login: str = "Copilot",
) -> ReviewCommentInfo:
    return ReviewCommentInfo(
        id=1,
        html_url="",
        path=path,
        body="finding",
        is_suppressed=is_suppressed,
        author_login=author_login,
    )


class TestCountPriorExecutablePostedFindings:
    """Tests for count_prior_executable_posted_findings."""

    def test_counts_only_posted_copilot_findings_on_executable_paths(self) -> None:
        provider = MagicMock()
        provider.list_all_review_comments.return_value = [
            _comment(path="agentic_devtools/state.py"),
            _comment(path="scripts/targeted-checks.sh"),
            _comment(path="specs/3672/spec.md"),
            _comment(path="agentic_devtools/state.py", is_suppressed=True),
            _comment(path="agentic_devtools/state.py", author_login="a-human"),
        ]

        assert count_prior_executable_posted_findings(provider, 11) == 2

    def test_returns_zero_without_comments(self) -> None:
        provider = MagicMock()
        provider.list_all_review_comments.return_value = []
        assert count_prior_executable_posted_findings(provider, 11) == 0

    def test_propagates_provider_errors(self) -> None:
        provider = MagicMock()
        provider.list_all_review_comments.side_effect = RuntimeError("API down")
        with pytest.raises(RuntimeError, match="API down"):
            count_prior_executable_posted_findings(provider, 11)
