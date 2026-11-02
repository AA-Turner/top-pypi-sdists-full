"""Tests for github_provider._is_transient_gh_failure()."""

from agentic_devtools.cli.ci.github_provider import _is_transient_gh_failure


def test_recognizes_rate_limit_text_as_transient() -> None:
    assert _is_transient_gh_failure("API rate limit exceeded")
    assert not _is_transient_gh_failure("permission denied")
