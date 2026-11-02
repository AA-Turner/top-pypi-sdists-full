"""Tests for GitHubActionsProvider.get_commit_range_diff_bytes()."""

from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_returns_lossless_compare_diff_bytes() -> None:
    """The raw compare-diff API preserves non-UTF-8 patch bytes."""
    expected = b"diff --git a/file.py b/file.py\n\xff"
    provider = GitHubActionsProvider(repo="owner/repo")

    with patch(
        "agentic_devtools.cli.ci.github_provider.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout=expected, stderr=b""),
    ):
        actual = provider.get_commit_range_diff_bytes("base", "head")

    assert actual == expected


def test_preserves_diff_context_that_resembles_response_headers() -> None:
    diff_body = (
        b"diff --git a/x b/x\n@@ -1,3 +1,3 @@\n HTTP/1.1 200 OK\n Header: unchanged diff context\n \n+new line\n"
    )
    response = (
        b"HTTP/2 200 OK\r\n"
        b"content-type: application/vnd.github.v3.diff\r\n"
        b"x-ratelimit-remaining: 80\r\n\r\n" + diff_body
    )
    provider = GitHubActionsProvider(repo="owner/repo")

    with patch(
        "agentic_devtools.cli.ci.github_provider.run_safe",
        return_value=SimpleNamespace(returncode=0, stdout=response, stderr=b""),
    ):
        assert provider.get_commit_range_diff_bytes("base", "head") == diff_body
