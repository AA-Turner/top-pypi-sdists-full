"""Tests for _refresh_pr_details_for_commit."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_commands import (
    _refresh_pr_details_for_commit,
)


class TestRefreshPrDetailsForCommit:
    """Tests for _refresh_pr_details_for_commit."""

    def test_system_exit_from_get_pull_request_details_is_caught_and_retried(
        self,
        tmp_path: Path,
    ) -> None:
        """SystemExit raised by get_pull_request_details() must not propagate; the loop retries.

        get_pull_request_details() calls sys.exit() on fetch failures. Without SystemExit
        in the exception handler, a transient failure on the first attempt terminates the
        process immediately instead of retrying up to _POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS
        times or reaching the controlled failure path (return None).
        """
        details_path = tmp_path / "pr-details.json"
        commit_hash = "abc1234"

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands._POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS",
                1,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands._POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS",
                0,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details",
                side_effect=SystemExit(1),
            ),
        ):
            result = _refresh_pr_details_for_commit(details_path, commit_hash)

        assert result is None

    def test_system_exit_retries_and_succeeds_on_second_attempt(
        self,
        tmp_path: Path,
    ) -> None:
        """After a SystemExit on attempt 1 the loop continues and returns data on attempt 2."""
        commit_hash = "abc1234"
        details_path = tmp_path / "pr-details.json"
        payload = {"pullRequest": {"lastMergeSourceCommit": {"commitId": commit_hash}}}
        details_path.write_text(json.dumps(payload))

        call_count = 0

        def _get_pr_details_side_effect() -> None:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise SystemExit(1)
            # Second call succeeds — details file already written above.

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands._POST_SYNC_PR_DETAILS_REFRESH_ATTEMPTS",
                2,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands._POST_SYNC_PR_DETAILS_REFRESH_DELAY_SECONDS",
                0,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.time.sleep",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details",
                side_effect=_get_pr_details_side_effect,
            ),
        ):
            result = _refresh_pr_details_for_commit(details_path, commit_hash)

        assert result == payload
        assert call_count == 2
