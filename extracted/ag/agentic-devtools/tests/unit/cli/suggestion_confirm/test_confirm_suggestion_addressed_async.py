"""Tests for confirm_suggestion_addressed_async."""

import json
from unittest.mock import MagicMock, call, patch

import pytest

from agentic_devtools.adapters.suggestion_confirm import SuggestionConfirmationRequest
from agentic_devtools.cli.suggestion_confirm import confirm_suggestion_addressed_async


class TestConfirmSuggestionAddressedAsync:
    """Validate background task dispatch and request snapshot isolation."""

    @patch("agentic_devtools.cli.suggestion_confirm.print_task_tracking_info")
    @patch("agentic_devtools.cli.suggestion_confirm.run_function_in_background")
    @patch("agentic_devtools.cli.suggestion_confirm.build_confirmation_request")
    def test_dispatches_validated_request_snapshot(
        self,
        mock_build: MagicMock,
        mock_run: MagicMock,
        mock_tracking: MagicMock,
    ) -> None:
        request = SuggestionConfirmationRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=12,
            discussion_id=34,
            commit_hash="abcdef",
            review_thread_id="PRRT_node",
        )
        mock_build.return_value = request
        mock_run.return_value = "task-1"

        confirm_suggestion_addressed_async(
            pull_request_id="12",
            thread_id="34",
            commit_hash="abcdef",
            provider="github",
            repository="owner/repo",
            review_thread_id="PRRT_node",
        )

        mock_build.assert_called_once_with(
            provider="github",
            repository="owner/repo",
            pull_request_id="12",
            discussion_id="34",
            commit_hash="abcdef",
            review_thread_id="PRRT_node",
        )
        assert mock_run.call_args == call(
            "agentic_devtools.cli.suggestion_confirm",
            "_confirmation_task",
            command_display_name="agdt-confirm-suggestion-addressed",
            args={"request": request.__dict__},
            func_kwargs={"request": request.__dict__},
        )
        assert mock_tracking.call_args_list == [call("task-1", "Confirming suggestion addressed")]

    @patch("agentic_devtools.cli.suggestion_confirm.print_task_tracking_info")
    @patch("agentic_devtools.cli.suggestion_confirm.run_function_in_background")
    @patch("agentic_devtools.cli.suggestion_confirm.build_confirmation_request")
    def test_each_call_snapshots_an_independent_request(
        self,
        mock_build: MagicMock,
        mock_run: MagicMock,
        mock_tracking: MagicMock,
    ) -> None:
        first_request = SuggestionConfirmationRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=1,
            discussion_id=1,
            commit_hash="abc",
            review_thread_id="PRRT_node",
        )
        second_request = SuggestionConfirmationRequest(
            provider="azure_devops", repository="repo", pull_request_id=2, discussion_id=2, commit_hash="def"
        )
        mock_build.side_effect = [first_request, second_request]
        mock_run.side_effect = ["task-1", "task-2"]

        confirm_suggestion_addressed_async(pull_request_id="1", thread_id="1", commit_hash="abc")
        confirm_suggestion_addressed_async(pull_request_id="2", thread_id="2", commit_hash="def")

        first_kwargs = mock_run.call_args_list[0].kwargs["func_kwargs"]["request"]
        second_kwargs = mock_run.call_args_list[1].kwargs["func_kwargs"]["request"]
        assert first_kwargs == first_request.__dict__
        assert second_kwargs == second_request.__dict__
        assert first_kwargs is not second_kwargs

    @patch("agentic_devtools.cli.suggestion_confirm.run_function_in_background")
    @patch("agentic_devtools.cli.suggestion_confirm.build_confirmation_request")
    def test_reports_invalid_request_and_exits_nonzero_without_dispatching(
        self,
        mock_build: MagicMock,
        mock_run: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_build.side_effect = ValueError("pull_request_id is required")

        with pytest.raises(SystemExit) as exc_info:
            confirm_suggestion_addressed_async(commit_hash="abc")

        assert exc_info.value.code == 1
        mock_run.assert_not_called()
        payload = json.loads(capsys.readouterr().out)
        assert payload["status"] == "invalid"
        assert payload["success"] is False
        assert "pull_request_id is required" in payload["diagnostics"][0]
