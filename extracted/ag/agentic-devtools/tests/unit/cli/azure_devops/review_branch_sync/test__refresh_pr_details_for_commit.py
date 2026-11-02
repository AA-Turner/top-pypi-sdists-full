"""Tests for _refresh_pr_details_for_commit."""

from typing import Any
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_branch_sync import (
    _refresh_pr_details_for_commit,
)


class TestRefreshPrDetailsForCommit:
    """Tests for _refresh_pr_details_for_commit."""

    def test_mismatched_commit_is_rejected(self, capsys) -> None:
        """PR details whose source commit differs from local HEAD are rejected."""
        payload = {"pullRequest": {"lastMergeSourceCommit": {"commitId": "different"}}}

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS",
                1,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS",
                0,
            ),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=payload,
            ),
        ):
            assert _refresh_pr_details_for_commit("expected") is None

        assert "did not match local HEAD" in capsys.readouterr().err

    def test_unexpected_response_type_is_rejected(self, capsys) -> None:
        """Non-dict PR details are rejected with a warning."""
        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS",
                1,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS",
                0,
            ),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=[],
            ),
        ):
            assert _refresh_pr_details_for_commit("expected") is None

        assert "had unexpected type 'list'" in capsys.readouterr().err

    def test_system_exit_from_get_pull_request_details_is_caught_and_retried(
        self,
    ) -> None:
        """SystemExit raised by get_pull_request_details() must not propagate; the loop retries.

        get_pull_request_details() calls sys.exit() on fetch failures. Without SystemExit
        in the exception handler, a transient failure on the first attempt terminates the
        process immediately instead of retrying up to _POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS
        times or reaching the controlled failure path (return None).
        """
        commit_hash = "abc1234"

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS",
                1,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS",
                0,
            ),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                side_effect=SystemExit(1),
            ),
        ):
            result = _refresh_pr_details_for_commit(commit_hash)

        assert result is None

    def test_system_exit_retries_and_succeeds_on_second_attempt(
        self,
    ) -> None:
        """After a SystemExit on attempt 1 the loop continues and returns data on attempt 2."""
        commit_hash = "abc1234"
        payload = {"pullRequest": {"lastMergeSourceCommit": {"commitId": commit_hash}}}

        call_count = 0

        def _get_pr_details_side_effect() -> dict[str, Any] | None:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise SystemExit(1)
            return payload

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS",
                2,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS",
                0,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync.time.sleep",
            ),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                side_effect=_get_pr_details_side_effect,
            ),
        ):
            result = _refresh_pr_details_for_commit(commit_hash)

        assert result == payload
        assert call_count == 2

    def test_runtime_error_retries_and_succeeds_on_second_attempt(self) -> None:
        """After a RuntimeError on attempt 1 the loop continues and returns data on attempt 2."""
        commit_hash = "abc1234"
        payload = {"pullRequest": {"lastMergeSourceCommit": {"commitId": commit_hash}}}

        call_count = 0

        def _get_pr_details_side_effect() -> dict[str, Any]:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("transient refresh failure")
            return payload

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS",
                2,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_branch_sync._POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS",
                0,
            ),
            patch("agentic_devtools.cli.azure_devops.review_branch_sync.time.sleep"),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                side_effect=_get_pr_details_side_effect,
            ),
        ):
            result = _refresh_pr_details_for_commit(commit_hash)

        assert result == payload
        assert call_count == 2
