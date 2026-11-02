"""Tests for confirm_suggestion_addressed_async_cli."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.suggestion_confirm import confirm_suggestion_addressed_async_cli


class TestConfirmSuggestionAddressedAsyncCli:
    """Validate argument parsing and forwarding to confirm_suggestion_addressed_async."""

    def test_forwards_all_parsed_options(self) -> None:
        with (
            patch(
                "sys.argv",
                [
                    "agdt-confirm-suggestion-addressed",
                    "--pull-request-id",
                    "12",
                    "--thread-id",
                    "34",
                    "--commit-hash",
                    "abcdef",
                    "--provider",
                    "github",
                    "--repository",
                    "owner/repo",
                    "--review-thread-id",
                    "PRRT_node",
                ],
            ),
            patch(
                "agentic_devtools.cli.suggestion_confirm.confirm_suggestion_addressed_async",
            ) as mock_async,
        ):
            confirm_suggestion_addressed_async_cli()

        mock_async.assert_called_once_with(
            pull_request_id="12",
            thread_id="34",
            commit_hash="abcdef",
            provider="github",
            repository="owner/repo",
            review_thread_id="PRRT_node",
        )

    def test_short_flags_and_repo_alias_are_forwarded(self) -> None:
        with (
            patch(
                "sys.argv",
                [
                    "agdt-confirm-suggestion-addressed",
                    "-p",
                    "12",
                    "-t",
                    "34",
                    "-c",
                    "abcdef",
                    "--repo",
                    "owner/repo",
                ],
            ),
            patch(
                "agentic_devtools.cli.suggestion_confirm.confirm_suggestion_addressed_async",
            ) as mock_async,
        ):
            confirm_suggestion_addressed_async_cli()

        mock_async.assert_called_once_with(
            pull_request_id="12",
            thread_id="34",
            commit_hash="abcdef",
            provider=None,
            repository="owner/repo",
            review_thread_id=None,
        )

    def test_omitted_options_default_to_none(self) -> None:
        with (
            patch("sys.argv", ["agdt-confirm-suggestion-addressed"]),
            patch(
                "agentic_devtools.cli.suggestion_confirm.confirm_suggestion_addressed_async",
            ) as mock_async,
        ):
            confirm_suggestion_addressed_async_cli()

        mock_async.assert_called_once_with(
            pull_request_id=None,
            thread_id=None,
            commit_hash=None,
            provider=None,
            repository=None,
            review_thread_id=None,
        )

    def test_help_flag_exits_cleanly(self) -> None:
        with patch("sys.argv", ["agdt-confirm-suggestion-addressed", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                confirm_suggestion_addressed_async_cli()
        assert exc_info.value.code == 0
