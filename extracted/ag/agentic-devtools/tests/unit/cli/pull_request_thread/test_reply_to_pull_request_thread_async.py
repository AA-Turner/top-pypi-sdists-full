"""Tests for reply_to_pull_request_thread_async."""

from unittest.mock import MagicMock, call, patch

from agentic_devtools.cli.pull_request_thread import (
    reply_to_pull_request_thread_async,
)


class TestReplyToPullRequestThreadAsync:
    """Validate background task dispatch and snapshot isolation."""

    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    @patch("agentic_devtools.cli.pull_request_thread.print_task_tracking_info")
    @patch("agentic_devtools.cli.pull_request_thread.run_function_in_background")
    def test_async_captures_request_snapshot(
        self,
        mock_run: MagicMock,
        mock_tracking: MagicMock,
        mock_from_state: MagicMock,
    ) -> None:
        mock_run.side_effect = ["task-1", "task-2"]
        mock_from_state.return_value = MagicMock(organization="org", project="project", repository="repo-from-state")

        reply_to_pull_request_thread_async(
            provider="github",
            repository="owner/repo",
            pull_request_id=12,
            discussion_id=34,
            content="immutable\n✓",
            resolve_thread=True,
            review_thread_id="PRRT_first",
        )
        reply_to_pull_request_thread_async(
            provider="azure_devops",
            repository="project/repo",
            pull_request_id=56,
            discussion_id=78,
            content="second reply",
            resolve_thread=False,
        )

        first_request = mock_run.call_args_list[0].kwargs["func_kwargs"]["request"]
        second_request = mock_run.call_args_list[1].kwargs["func_kwargs"]["request"]
        assert first_request == {
            "provider": "github",
            "repository": "owner/repo",
            "pull_request_number": 12,
            "discussion_id": 34,
            "body": "immutable\n✓",
            "resolve": True,
            "review_thread_id": "PRRT_first",
            "dry_run": False,
        }
        assert second_request == {
            "provider": "azure_devops",
            "repository": "project/repo",
            "pull_request_number": 56,
            "discussion_id": 78,
            "body": "second reply",
            "resolve": False,
            "review_thread_id": None,
            "dry_run": False,
            "azure_organization": "org",
            "azure_project": "project",
        }
        assert first_request is not second_request
        assert mock_tracking.call_args_list == [
            call("task-1", "Replying to pull request thread"),
            call("task-2", "Replying to pull request thread"),
        ]
