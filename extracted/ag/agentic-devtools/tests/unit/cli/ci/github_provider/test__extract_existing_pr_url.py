"""Tests for _extract_existing_pr_url()."""

from agentic_devtools.cli.ci.github_provider import _extract_existing_pr_url


class TestExtractExistingPrUrl:
    """Idempotency helper for create_pull_request."""

    def test_extracts_url_from_already_exists_message(self) -> None:
        text = (
            'a pull request for branch "audit/instruction-update-abc" into branch "main" already exists:\n'
            "https://github.com/swai-factory/agentic-devtools/pull/2460"
        )
        assert _extract_existing_pr_url(text) == "https://github.com/swai-factory/agentic-devtools/pull/2460"

    def test_returns_empty_when_not_already_exists(self) -> None:
        # A URL alone (without the "already exists" signal) is NOT treated as reuse.
        text = "some other gh error: https://github.com/o/r/pull/9"
        assert _extract_existing_pr_url(text) == ""

    def test_returns_empty_when_already_exists_but_no_url(self) -> None:
        assert _extract_existing_pr_url("a pull request already exists somewhere") == ""

    def test_case_insensitive_match(self) -> None:
        text = "Already Exists:\nhttps://github.com/o/r/pull/12"
        assert _extract_existing_pr_url(text) == "https://github.com/o/r/pull/12"

    def test_extracts_github_enterprise_server_url(self) -> None:
        """GHES hosts use a custom domain; the regex must not be hardcoded to github.com."""
        text = (
            'a pull request for branch "audit/batch-abc" into branch "main" already exists:\n'
            "https://github.mycompany.com/owner/repo/pull/42"
        )
        assert _extract_existing_pr_url(text) == "https://github.mycompany.com/owner/repo/pull/42"
