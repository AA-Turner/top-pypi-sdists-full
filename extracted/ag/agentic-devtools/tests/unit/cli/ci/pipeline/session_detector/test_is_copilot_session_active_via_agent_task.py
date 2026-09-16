"""Tests for is_copilot_session_active_via_agent_task."""

import json
import subprocess
from unittest.mock import patch

from agentic_devtools.cli.ci.pipeline.session_detector import (
    is_copilot_session_active_via_agent_task,
)


class TestIsCopilotSessionActiveViaAgentTask:
    """Tests for the gh agent-task based session detector."""

    def _make_result(self, *, stdout: str = "", returncode: int = 0) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr="")

    def test_running_task_returns_true(self) -> None:
        """A running task for the target PR returns True."""
        tasks = [
            {
                "id": "task-1",
                "state": "in_progress",
                "repository": "owner/repo",
                "pullRequestNumber": 42,
                "createdAt": "2024-01-01T00:00:00Z",
            },
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_queued_task_returns_true(self) -> None:
        tasks = [
            {
                "id": "task-1",
                "state": "queued",
                "repository": "owner/repo",
                "pullRequestNumber": 42,
                "createdAt": "2024-01-01T00:00:00Z",
            }
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_idle_and_waiting_for_user_tasks_return_true(self) -> None:
        tasks = [
            {"id": "task-1", "state": "idle", "repository": "owner/repo", "pullRequestNumber": 42},
            {"id": "task-2", "state": "waiting_for_user", "repository": "owner/repo", "pullRequestNumber": 42},
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_completed_task_returns_false(self) -> None:
        tasks = [
            {
                "id": "task-1",
                "state": "completed",
                "repository": "owner/repo",
                "pullRequestNumber": 42,
                "createdAt": "2024-01-01T00:00:00Z",
            }
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is False

    def test_stopped_task_returns_false(self) -> None:
        tasks = [
            {
                "id": "task-1",
                "state": "stopped",
                "repository": "owner/repo",
                "pullRequestNumber": 42,
                "createdAt": "2024-01-01T00:00:00Z",
            }
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is False

    def test_empty_list_returns_false(self) -> None:
        result = self._make_result(stdout="[]")
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is False

    def test_different_pr_number_returns_false(self) -> None:
        """Tasks for a different PR do not affect the result."""
        tasks = [
            {
                "id": "task-1",
                "state": "in_progress",
                "repository": "owner/repo",
                "pullRequestNumber": 99,
                "createdAt": "2024-01-01T00:00:00Z",
            },
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is False

    def test_different_repository_does_not_match(self) -> None:
        """Tasks for a different repository do not affect the result."""
        tasks = [{"id": "task-1", "state": "in_progress", "repository": "other/repo", "pullRequestNumber": 42}]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is False

    def test_mixed_status_returns_true(self) -> None:
        """If any task for the PR is in an active status, returns True."""
        tasks = [
            {
                "id": "task-1",
                "state": "completed",
                "repository": "owner/repo",
                "pullRequestNumber": 42,
                "createdAt": "2024-01-01T00:00:00Z",
            },
            {
                "id": "task-2",
                "state": "running",
                "repository": "owner/repo",
                "pullRequestNumber": 42,
                "createdAt": "2024-01-01T01:00:00Z",
            },
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_timeout_returns_unknown(self) -> None:
        """Timeout results in an unavailable session state."""
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=subprocess.TimeoutExpired(cmd="gh", timeout=10),
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_nonzero_exit_returns_unknown(self) -> None:
        """A non-zero exit code results in an unavailable session state."""
        result = self._make_result(stdout="", returncode=1)
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_malformed_json_returns_unknown(self) -> None:
        """Malformed JSON results in an unavailable session state."""
        result = self._make_result(stdout="not json at all")
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_missing_binary_returns_unknown(self) -> None:
        """A missing gh binary results in an unavailable session state."""
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=FileNotFoundError("gh not found")
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_permission_error_returns_unknown(self) -> None:
        """PermissionError results in an unavailable session state."""
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=PermissionError("permission denied"),
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_os_error_returns_unknown(self) -> None:
        """OSError results in an unavailable session state."""
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=OSError("general OS error")
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_non_list_json_returns_unknown(self) -> None:
        """Non-list JSON results in an unavailable session state."""
        result = self._make_result(stdout='{"error": "something"}')
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_non_dict_items_are_ignored(self) -> None:
        """Non-dict list items are ignored while scanning tasks."""
        tasks = [
            "unexpected-string",
            {"id": "task-1", "state": "running", "repository": "owner/repo", "pullRequestNumber": 42},
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_non_dict_item_without_active_task_returns_unknown(self) -> None:
        """A non-dict task record makes an otherwise inactive inventory unknown."""
        result = self._make_result(stdout=json.dumps(["unexpected-string"]))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_missing_pull_request_number_returns_unknown(self) -> None:
        """A task record without a pull request number cannot prove inactivity."""
        result = self._make_result(stdout=json.dumps([{"state": "completed", "repository": "owner/repo"}]))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_missing_target_task_status_returns_unknown(self) -> None:
        """A target task without a status cannot prove inactivity."""
        result = self._make_result(stdout=json.dumps([{"repository": "owner/repo", "pullRequestNumber": 42}]))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_unknown_target_task_status_returns_unknown(self) -> None:
        """An unrecognized target task status cannot prove inactivity."""
        result = self._make_result(
            stdout=json.dumps(
                [{"id": "task-1", "state": "paused", "repository": "owner/repo", "pullRequestNumber": 42}]
            )
        )
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_missing_repository_returns_unknown(self) -> None:
        """A task record without a repository cannot prove inactivity."""
        result = self._make_result(stdout=json.dumps([{"state": "completed", "pullRequestNumber": 42}]))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_reaching_inventory_limit_returns_unknown(self) -> None:
        """A viewer-wide inventory at the fetch limit may be truncated."""
        tasks = [
            {"id": f"task-{index}", "state": "completed", "repository": "other/repo", "pullRequestNumber": 99}
            for index in range(1000)
        ]
        result = self._make_result(stdout=json.dumps(tasks))
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_calls_run_safe_with_correct_args(self) -> None:
        """Verify run_safe is called with the correct arguments and flags."""
        result = self._make_result(stdout="[]")
        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", return_value=result) as mock_run:
            is_copilot_session_active_via_agent_task("owner/repo", 42, timeout_seconds=15)
            mock_run.assert_called_once_with(
                [
                    "gh",
                    "agent-task",
                    "list",
                    "--limit",
                    "1000",
                    "--json",
                    "id,state,repository,pullRequestNumber,createdAt",
                ],
                capture_output=True,
                text=True,
                shell=False,
                timeout=15,
            )

    def test_custom_timeout(self) -> None:
        """Custom timeout_seconds is forwarded to subprocess.run."""
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=subprocess.TimeoutExpired(cmd="gh", timeout=5),
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42, timeout_seconds=5) is None

    def test_gh_agent_task_fails_rest_api_active_task_by_number(self) -> None:
        """When gh agent-task list fails, REST API finds active task by PR number."""
        cli_result = self._make_result(stdout="", returncode=1)
        rest_tasks = {
            "tasks": [
                {"id": "task-rest-1", "state": "in_progress", "pullRequestNumber": 42},
            ]
        }
        rest_result = self._make_result(stdout=json.dumps(rest_tasks), returncode=0)

        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=[cli_result, rest_result]):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_gh_agent_task_fails_rest_api_active_task_by_name(self) -> None:
        """When gh agent-task list fails, REST API matches active task by name."""
        cli_result = self._make_result(stdout="", returncode=1)
        rest_tasks = {
            "tasks": [
                {"id": "task-rest-2", "state": "running", "name": "Repairing review feedback for PR #42"},
            ]
        }
        rest_result = self._make_result(stdout=json.dumps(rest_tasks), returncode=0)

        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=[cli_result, rest_result]):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_gh_agent_task_fails_rest_api_active_task_by_artifacts(self) -> None:
        """When gh agent-task list fails, REST API matches active task by artifacts."""
        cli_result = self._make_result(stdout="", returncode=1)
        rest_tasks_pull = {
            "tasks": [
                {
                    "id": "task-rest-3",
                    "state": "queued",
                    "artifacts": [
                        "not-a-dict",
                        {"type": "other", "data": {}},
                        {"type": "pull", "data": "not-a-dict"},
                        {"type": "pull", "data": {"number": 999}},
                        {"type": "branch", "data": {"head_ref": "feature/unrelated"}},
                        {"type": "pull", "data": {"number": 42}},
                    ],
                },
            ]
        }
        rest_result = self._make_result(stdout=json.dumps(rest_tasks_pull), returncode=0)

        with patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=[cli_result, rest_result]):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

        # Also test branch artifact matching
        rest_tasks_branch = {
            "tasks": [
                {
                    "id": "task-rest-4",
                    "state": "queued",
                    "artifacts": [
                        {"type": "branch", "data": {"head_ref": "copilot/pr-42-fix"}},
                    ],
                },
            ]
        }
        rest_result_branch = self._make_result(stdout=json.dumps(rest_tasks_branch), returncode=0)
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=[cli_result, rest_result_branch],
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is True

    def test_gh_agent_task_fails_rest_api_confirms_inactive(self) -> None:
        """When gh agent-task list fails, REST API confirms no active task exists."""
        cli_result = self._make_result(stdout="", returncode=1)
        rest_tasks = {
            "tasks": [
                "not-a-dict",
                {"id": "t-no-artifacts", "state": "completed"},
                {
                    "id": "t-unmatched-artifacts",
                    "state": "completed",
                    "artifacts": [
                        {"type": "other", "data": {}},
                        {"type": "pull", "data": {"number": 999}},
                    ],
                },
                {"id": "task-rest-5", "state": "completed", "pullRequestNumber": 42},
                {"id": "task-rest-6", "state": "in_progress", "pullRequestNumber": 99},
            ]
        }
        rest_result = self._make_result(stdout=json.dumps(rest_tasks), returncode=0)

        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=[cli_result, rest_result],
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is False

    def test_rest_api_failures_and_errors(self) -> None:
        """REST API error handling: malformed json, bad shape, timeout."""
        cli_result = self._make_result(stdout="", returncode=1)

        # Non-zero returncode on rest API
        rest_bad_code = self._make_result(stdout="", returncode=1)
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=[cli_result, rest_bad_code],
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

        # Malformed JSON
        rest_bad_json = self._make_result(stdout="bad-json", returncode=0)
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=[cli_result, rest_bad_json],
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

        # Non-dict JSON
        rest_non_dict = self._make_result(stdout="[]", returncode=0)
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=[cli_result, rest_non_dict],
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

        # Timeout on REST API
        with patch(
            "agentic_devtools.cli.ci.pipeline.session_detector.run_safe",
            side_effect=[cli_result, subprocess.TimeoutExpired(cmd="gh api", timeout=5)],
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42) is None

    def test_fallback_to_provider_issue_events(self) -> None:
        """When both CLI and REST fail, falls back to provider.list_pr_issue_events."""
        from unittest.mock import MagicMock

        cli_result = self._make_result(stdout="", returncode=1)
        rest_result = self._make_result(stdout="", returncode=1)

        provider = MagicMock()
        # Fallback says inactive
        with (
            patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=[cli_result, rest_result]),
            patch(
                "agentic_devtools.cli.ci.pipeline.session_detector.is_copilot_session_active",
                return_value=False,
            ) as mock_events,
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42, provider=provider) is False
            mock_events.assert_called_once_with(provider, 42)

        # Fallback says active
        with (
            patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=[cli_result, rest_result]),
            patch("agentic_devtools.cli.ci.pipeline.session_detector.is_copilot_session_active", return_value=True),
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42, provider=provider) is True

        # Fallback raises exception -> None
        with (
            patch("agentic_devtools.cli.ci.pipeline.session_detector.run_safe", side_effect=[cli_result, rest_result]),
            patch(
                "agentic_devtools.cli.ci.pipeline.session_detector.is_copilot_session_active",
                side_effect=RuntimeError("events error"),
            ),
        ):
            assert is_copilot_session_active_via_agent_task("owner/repo", 42, provider=provider) is None
