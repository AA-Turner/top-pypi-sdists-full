"""Tests for _is_authorization_failure()."""

from agentic_devtools.cli.ci.watchdog_command import _is_authorization_failure


class TestIsAuthorizationFailure:
    """Authorization-error classifier behavior."""

    def test_matches_known_authorization_error_patterns(self) -> None:
        assert _is_authorization_failure("HTTP/2.0 401 Unauthorized")
        assert _is_authorization_failure("Resource not accessible by personal access token")
        assert _is_authorization_failure("repository.pullRequests denied")

    def test_does_not_match_non_authorization_failures(self) -> None:
        assert not _is_authorization_failure("workflow dispatch failed")
