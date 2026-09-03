"""Tests for ai_pr_loop_watchdog_command()."""

import json
import os
import sys
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.reconciliation.models import CooldownProbe, CooldownState, ProbeStatus, QueueState
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.ci.scheduler import EligiblePR


class TestAiPrLoopWatchdogCommand:
    """CLI entry point for agdt-ai-pr-loop-watchdog."""

    def test_seeds_cooldown_state_from_latest_throttler_run(self) -> None:
        from agentic_devtools.cli.ci.watchdog_command import _seed_cooldown_state

        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        state = _seed_cooldown_state(
            {
                "id": 123,
                "status": "completed",
                "conclusion": "success",
                "updated_at": "2026-07-27T10:00:00Z",
            },
            now,
        )

        assert state is not None
        assert state.cooldown_generation_id == "throttler-123"
        assert state.resume_at == now - timedelta(seconds=30) + timedelta(seconds=60)

    def test_dispatches_when_not_throttled_and_eligible(self, capsys) -> None:
        updated_at = "2026-07-27T10:00:00Z"
        now = datetime(2026, 7, 27, 10, 5, 0, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r", "--default-branch", "main"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=2),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._load_cooldown_state",
                return_value=CooldownState("gh", "cred1", "generation-1", now),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_provider_cls.return_value.list_eligible_prs.return_value = [EligiblePR(number=123, created_at="")]
            mock_gh_api.side_effect = [
                json.dumps(
                    {"workflow_runs": [{"status": "completed", "conclusion": "success", "updated_at": updated_at}]}
                ),
                "",
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        out = capsys.readouterr().out
        payload = json.loads(out.splitlines()[-1])
        assert payload["decision"] == "dispatched"
        assert payload["dispatched"] is True
        assert payload["due_probe_count"] == 2
        assert payload["eligible_count"] == 1
        assert payload["throttled"] is False
        assert payload["default_branch"] == "main"
        assert "::notice::ai-pr-loop-watchdog evaluated 2 due probe(s)" in out
        dispatch_call = mock_gh_api.call_args_list[1]
        assert dispatch_call.kwargs["method"] == "POST"
        assert dispatch_call.kwargs["body"] == {"ref": "main"}

    def test_skips_when_throttled_in_progress(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=3) as mock_probe_wakeup,
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "in_progress", "conclusion": None, "updated_at": "2026-07-27T10:00:00Z"}
                        ]
                    }
                ),
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "throttled"
        assert payload["dispatched"] is False
        assert payload["throttled"] is True
        assert payload["throttle_reason"] == "in_progress"
        assert payload["due_probe_count"] == 3
        assert payload["eligible_count"] is None
        mock_probe_wakeup.assert_called_once_with(repo="o/r")

    def test_skips_when_no_eligible_prs(self, capsys) -> None:
        updated_at = "2026-07-27T10:00:00Z"
        now = datetime(2026, 7, 27, 10, 5, 0, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_provider_cls.return_value.list_eligible_prs.return_value = []
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps(
                    {"workflow_runs": [{"status": "completed", "conclusion": "success", "updated_at": updated_at}]}
                ),
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "no_eligible_prs"
        assert payload["dispatched"] is False
        assert payload["eligible_count"] == 0

    def test_retries_immediately_when_last_run_failed(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_provider_cls.return_value.list_eligible_prs.return_value = [EligiblePR(number=555, created_at="")]
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "failure", "updated_at": "2026-07-27T10:04:59Z"}
                        ]
                    }
                ),
                "",
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "dispatched"
        assert payload["dispatched"] is True
        assert payload["throttled"] is False
        assert payload["throttle_reason"] == "last_run_not_success"

    def test_exits_10_when_gh_missing(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value=None),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            try:
                ai_pr_loop_watchdog_command()
            except SystemExit as exc:
                assert exc.code == 10
            else:
                raise AssertionError("Expected SystemExit(10)")

    def test_cooldown_throttle_path(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T10:00:00Z"}
                        ]
                    }
                ),
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "throttled"
        assert payload["throttle_reason"] == "cooldown"
        assert payload["eligible_count"] is None

    def test_provider_cooldown_pauses_without_listing_or_dispatching(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r", "--default-branch", "main"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.active_cooldown",
                return_value=("github:GH_TOKEN", CooldownRecord(resume_at=now.timestamp() + 120, source="fallback")),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0) as mock_probe_wakeup,
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "rate_limit_paused"
        assert payload["cooldown_key"] == "github:GH_TOKEN"
        assert payload["default_branch"] == "main"
        assert payload["elapsed_seconds"] is None
        assert payload["due_probe_count"] == 0
        cooldown_state = mock_probe_wakeup.call_args.kwargs["cooldown_state"]
        assert cooldown_state.provider_identity == "github"
        assert cooldown_state.credential_identity == "GH_TOKEN"
        assert cooldown_state.resume_at == datetime.fromtimestamp(now.timestamp() + 120, UTC)
        mock_gh_api.assert_not_called()
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()

    def test_provider_cooldown_honors_auxiliary_loop_credentials(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        cooldown_payload = (
            '{"provider_cooldowns":{"github:AGDT_PR_APPROVER_PAT":'
            '{"resume_at":1785146550,"source":"retry-after","updated_at":1785146400}}}'
        )
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r", "--default-branch", "main"]),
            patch.dict(
                os.environ,
                {
                    "AI_PR_LOOP_CREDENTIAL_IDENTITY": "SPECKIT_PR_TOKEN",
                    "REPO_VARIABLE_WRITER_PAT": "writer",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                side_effect=[
                    json.dumps({"default_branch": "main"}),
                    json.dumps({"workflow_runs": []}),
                    "",
                ],
            ) as mock_gh_api,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0) as mock_probe_wakeup,
        ):
            mock_provider_cls.return_value.get_variable.return_value = cooldown_payload
            mock_provider_cls.return_value.list_eligible_prs.return_value = []

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "rate_limit_paused"
        assert payload["cooldown_key"] == "github:AGDT_PR_APPROVER_PAT"
        assert payload["dispatched"] is False
        assert payload["due_probe_count"] == 0
        assert mock_probe_wakeup.call_args.kwargs["cooldown_state"].credential_identity == "AGDT_PR_APPROVER_PAT"
        assert payload["eligible_count"] is None
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()
        mock_gh_api.assert_not_called()

    def test_provider_cooldown_logs_due_probe_failure_and_stays_paused(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r", "--default-branch", "main"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.active_cooldown",
                return_value=("github:GH_TOKEN", CooldownRecord(resume_at=now.timestamp() + 120, source="fallback")),
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup",
                side_effect=RuntimeError("queue unavailable"),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.logger") as mock_logger,
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "rate_limit_paused"
        assert payload["due_probe_count"] == 0
        mock_logger.warning.assert_called_once()
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()
        mock_gh_api.assert_not_called()

    def test_cooldown_gate_emits_sanitized_fields_and_outputs(self, capsys, tmp_path) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-ai-pr-loop-watchdog", "--mode", "cooldown-gate", "--repo", "o/r"],
            ),
            patch.dict(
                os.environ,
                {
                    "GITHUB_OUTPUT": str(github_output),
                    "AI_PR_LOOP_CREDENTIAL_IDENTITY": "SPECKIT_PR_TOKEN",
                    "REPO_VARIABLE_WRITER_PAT": "writer",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
        ):
            mock_provider_cls.return_value.get_variable.return_value = (
                '{"provider_cooldowns":{"github:SPECKIT_PR_TOKEN":'
                '{"resume_at":1785146550,"reason":"rate_limit","source":"retry-after","updated_at":1785146400}}}'
            )
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        out_lines = capsys.readouterr().out.splitlines()
        assert "provider=github credential=SPECKIT_PR_TOKEN reason=rate_limit source=retry-after" in out_lines[0]
        payload = json.loads(out_lines[-1])
        assert payload["cooldown_active"] is True
        assert payload["cooldown_provider"] == "github"
        assert payload["cooldown_credential"] == "SPECKIT_PR_TOKEN"
        assert payload["cooldown_reason"] == "rate_limit"
        assert payload["cooldown_source"] == "retry-after"
        assert github_output.read_text(encoding="utf-8").splitlines() == [
            "cooldown_active=true",
            "cooldown_remaining_seconds=120",
        ]

    def test_cooldown_gate_reports_inactive_when_no_cooldown(self, capsys, tmp_path) -> None:
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-ai-pr-loop-watchdog", "--mode", "cooldown-gate", "--repo", "o/r"],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
        ):
            mock_provider_cls.return_value.get_variable.return_value = "{}"
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload == {"cooldown_active": False}
        assert github_output.read_text(encoding="utf-8").splitlines() == [
            "cooldown_active=false",
            "cooldown_remaining_seconds=0",
        ]

    def test_throttles_when_conclusion_missing_on_completed_run(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": None, "updated_at": "2026-07-27T10:00:00Z"}
                        ]
                    }
                ),
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "throttled"
        assert payload["throttle_reason"] == "cooldown"
        assert payload["eligible_count"] is None

    def test_dispatches_when_no_prior_runs(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_provider_cls.return_value.list_eligible_prs.return_value = [EligiblePR(number=901, created_at="")]
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps({"workflow_runs": []}),
                "",
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "dispatched"
        assert payload["throttle_reason"] == "no_prior_run"

    def test_dispatches_when_latest_run_payload_is_not_dict(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_provider_cls.return_value.list_eligible_prs.return_value = [EligiblePR(number=902, created_at="")]
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps({"workflow_runs": [123]}),
                "",
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "dispatched"
        assert payload["throttle_reason"] == "no_prior_run"

    def test_dispatches_when_latest_run_timestamp_is_invalid(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_provider_cls.return_value.list_eligible_prs.return_value = [EligiblePR(number=903, created_at="")]
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps({"workflow_runs": [{"status": "completed", "conclusion": "success", "updated_at": "bad"}]}),
                "",
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "dispatched"
        assert payload["throttle_reason"] == "no_prior_run"

    def test_cooldown_availability_returns_true_when_no_blocking_probes(self) -> None:
        now = datetime.now(UTC)
        state = QueueState(
            repo="o/r",
            revision=1,
            items={},
            records=[],
            quarantines=[],
            probes=[
                CooldownProbe(
                    probe_id="probe-1",
                    provider_identity="gh",
                    credential_identity="COPILOT_GITHUB_TOKEN",
                    cooldown_generation_id="gen-1",
                    status=ProbeStatus.SUCCEEDED,
                    scheduled_at=now - timedelta(minutes=1),
                )
            ],
        )

        class _Store:
            def load(self) -> QueueState:
                return state

        with patch("agentic_devtools.cli.ci.watchdog_command.QueueStore", return_value=_Store()):
            from agentic_devtools.cli.ci.watchdog_command import _cooldown_availability

            available, reason = _cooldown_availability("o/r")

        assert available is True
        assert reason == "available"

    def test_cooldown_availability_blocks_pending_probe(self) -> None:
        now = datetime.now(UTC)
        state = QueueState(
            repo="o/r",
            revision=1,
            items={},
            records=[],
            quarantines=[],
            probes=[
                CooldownProbe(
                    probe_id="probe-1",
                    provider_identity="gh",
                    credential_identity="COPILOT_GITHUB_TOKEN",
                    cooldown_generation_id="gen-1",
                    status=ProbeStatus.PENDING,
                    scheduled_at=now - timedelta(minutes=1),
                )
            ],
        )

        class _Store:
            def load(self) -> QueueState:
                return state

        with patch("agentic_devtools.cli.ci.watchdog_command.QueueStore", return_value=_Store()):
            from agentic_devtools.cli.ci.watchdog_command import _cooldown_availability

            available, reason = _cooldown_availability("o/r")

        assert available is False
        assert reason == "cooldown_pending"

    def test_cooldown_availability_ignores_superseded_alertable_generation(self) -> None:
        now = datetime.now(UTC)
        state = QueueState(
            repo="o/r",
            revision=1,
            items={},
            records=[],
            quarantines=[],
            probes=[
                CooldownProbe(
                    probe_id="probe-old",
                    provider_identity="gh",
                    credential_identity="COPILOT_GITHUB_TOKEN",
                    cooldown_generation_id="generation-1",
                    status=ProbeStatus.ALERTABLE,
                    scheduled_at=now - timedelta(minutes=5),
                    resume_at=now - timedelta(minutes=5),
                ),
                CooldownProbe(
                    probe_id="probe-new",
                    provider_identity="gh",
                    credential_identity="COPILOT_GITHUB_TOKEN",
                    cooldown_generation_id="generation-2",
                    status=ProbeStatus.SUCCEEDED,
                    scheduled_at=now - timedelta(minutes=1),
                    resume_at=now - timedelta(minutes=1),
                ),
            ],
        )

        class _Store:
            def load(self) -> QueueState:
                return state

        with patch("agentic_devtools.cli.ci.watchdog_command.QueueStore", return_value=_Store()):
            from agentic_devtools.cli.ci.watchdog_command import _cooldown_availability

            available, reason = _cooldown_availability("o/r")

        assert available is True
        assert reason == "available"

    def test_exits_one_when_default_branch_missing(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value=json.dumps({})),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            try:
                ai_pr_loop_watchdog_command()
            except SystemExit as exc:
                assert exc.code == 1
            else:
                raise AssertionError("Expected SystemExit(1)")

    def test_parse_timestamp_edge_cases(self) -> None:
        from agentic_devtools.cli.ci.watchdog_command import _parse_timestamp

        assert _parse_timestamp("") is None
        assert _parse_timestamp("not-a-date") is None
        parsed = _parse_timestamp("2026-07-27T10:00:00")
        assert parsed is not None
        assert parsed.tzinfo is not None

    def test_elapsed_seconds_clamped_to_zero_on_clock_skew(self, capsys) -> None:
        # updated_at is AFTER now (simulates clock skew where runner clock is behind GitHub)
        # Without clamping this would produce negative elapsed_seconds, causing perpetual cooldown
        # with confusing negative telemetry. With clamping, elapsed_seconds=0 < COOLDOWN_SECONDS,
        # so the run is correctly throttled with elapsed_seconds=0.
        now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            # updated_at is 5 seconds AFTER now — would produce elapsed_seconds=-5 without clamping
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T10:00:05Z"}
                        ]
                    }
                ),
            ]

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "throttled"
        assert payload["throttle_reason"] == "cooldown"
        assert payload["elapsed_seconds"] == 0
        assert payload["eligible_count"] is None

    def test_blocks_dispatch_when_cooldown_not_available(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=1),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._cooldown_availability",
                return_value=(False, "cooldown_failed"),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps({"workflow_runs": []}),
            ]
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "cooldown_blocked"
        assert payload["dispatched"] is False
        assert payload["availability_established"] is False
        assert payload["availability_reason"] == "cooldown_failed"
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()

    def test_blocks_dispatch_when_due_probe_wakeup_raises(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch(
                "agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup",
                side_effect=RuntimeError("storage unavailable"),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps({"workflow_runs": []}),
            ]
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "cooldown_blocked"
        assert payload["availability_reason"] == "cooldown_state_unknown"
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()

    def test_preserves_due_probe_count_when_cooldown_lookup_raises(self, capsys) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=3),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._cooldown_availability",
                side_effect=RuntimeError("state decode failed"),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_gh_api.side_effect = [
                json.dumps({"default_branch": "main"}),
                json.dumps({"workflow_runs": []}),
            ]
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "cooldown_blocked"
        assert payload["due_probe_count"] == 3
        assert payload["availability_reason"] == "cooldown_state_unknown"
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()

    def test_loads_active_cooldown_state_for_probe_wakeup(self) -> None:
        from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
        from agentic_devtools.cli.ci.watchdog_command import _load_cooldown_state

        scheduled_at = datetime.now(UTC)
        probe = CooldownProbe(
            probe_id="probe-1",
            provider_identity="gh",
            credential_identity="cred1",
            cooldown_generation_id="generation-1",
            status=ProbeStatus.PENDING,
            scheduled_at=scheduled_at,
            resume_at=scheduled_at,
        )
        store = QueueStore(repo="o/r", backing=InMemoryBackingStore())
        state = store.load()
        state.probes.append(
            CooldownProbe(
                probe_id="completed-probe",
                provider_identity="gh",
                credential_identity="cred1",
                cooldown_generation_id="generation-0",
                status=ProbeStatus.SUCCEEDED,
                scheduled_at=scheduled_at,
            )
        )
        state.probes.append(probe)
        store.save(state, expected_revision=state.revision)
        with patch("agentic_devtools.cli.ci.watchdog_command.QueueStore", return_value=store):
            cooldown = _load_cooldown_state("o/r")

        assert cooldown == CooldownState("gh", "cred1", "generation-1", scheduled_at)

    def test_load_cooldown_state_ignores_superseded_terminal_generation(self) -> None:
        from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
        from agentic_devtools.cli.ci.watchdog_command import _load_cooldown_state

        older = datetime.now(UTC) - timedelta(minutes=10)
        newer = datetime.now(UTC) - timedelta(minutes=2)
        store = QueueStore(repo="o/r", backing=InMemoryBackingStore())
        state = store.load()
        state.probes.extend(
            [
                CooldownProbe(
                    probe_id="probe-old",
                    provider_identity="gh",
                    credential_identity="cred1",
                    cooldown_generation_id="generation-1",
                    status=ProbeStatus.ALERTABLE,
                    scheduled_at=older,
                    resume_at=older,
                ),
                CooldownProbe(
                    probe_id="probe-new",
                    provider_identity="gh",
                    credential_identity="cred1",
                    cooldown_generation_id="generation-2",
                    status=ProbeStatus.PENDING,
                    scheduled_at=newer,
                    resume_at=newer,
                ),
            ]
        )
        store.save(state, expected_revision=state.revision)

        with patch("agentic_devtools.cli.ci.watchdog_command.QueueStore", return_value=store):
            cooldown = _load_cooldown_state("o/r")

        assert cooldown is not None
        assert cooldown.cooldown_generation_id == "generation-2"
        assert cooldown.probe_status == ProbeStatus.PENDING

    def test_load_cooldown_state_skips_terminal_candidate_before_returning_active_one(self) -> None:
        from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
        from agentic_devtools.cli.ci.watchdog_command import _load_cooldown_state

        t1 = datetime.now(UTC) - timedelta(minutes=1)
        t2 = datetime.now(UTC) - timedelta(minutes=3)
        store = QueueStore(repo="o/r", backing=InMemoryBackingStore())
        state = store.load()
        state.probes.extend(
            [
                CooldownProbe(
                    probe_id="probe-cred1-terminal",
                    provider_identity="gh",
                    credential_identity="cred1",
                    cooldown_generation_id="generation-1",
                    status=ProbeStatus.SUCCEEDED,
                    scheduled_at=t1,
                    resume_at=t1,
                ),
                CooldownProbe(
                    probe_id="probe-cred2-active",
                    provider_identity="gh",
                    credential_identity="cred2",
                    cooldown_generation_id="generation-1",
                    status=ProbeStatus.PENDING,
                    scheduled_at=t2,
                    resume_at=t2,
                ),
            ]
        )
        store.save(state, expected_revision=state.revision)

        with patch("agentic_devtools.cli.ci.watchdog_command.QueueStore", return_value=store):
            cooldown = _load_cooldown_state("o/r")

        assert cooldown is not None
        assert cooldown.credential_identity == "cred2"
        assert cooldown.probe_status == ProbeStatus.PENDING

    def test_latest_probe_generation_candidates_keeps_newest_per_identity(self) -> None:
        from agentic_devtools.cli.ci.watchdog_command import _latest_probe_generation_candidates

        newer = datetime.now(UTC)
        older = newer - timedelta(minutes=2)
        candidates = _latest_probe_generation_candidates(
            [
                CooldownProbe(
                    probe_id="probe-new",
                    provider_identity="gh",
                    credential_identity="cred1",
                    cooldown_generation_id="generation-2",
                    status=ProbeStatus.PENDING,
                    scheduled_at=newer,
                ),
                CooldownProbe(
                    probe_id="probe-old",
                    provider_identity="gh",
                    credential_identity="cred1",
                    cooldown_generation_id="generation-1",
                    status=ProbeStatus.ALERTABLE,
                    scheduled_at=older,
                ),
            ]
        )

        assert len(candidates) == 1
        assert candidates[0].probe_id == "probe-new"

    def test_loads_no_cooldown_state_when_queue_has_no_probes(self) -> None:
        from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
        from agentic_devtools.cli.ci.watchdog_command import _load_cooldown_state

        store = QueueStore(repo="o/r", backing=InMemoryBackingStore())
        with patch("agentic_devtools.cli.ci.watchdog_command.QueueStore", return_value=store):
            assert _load_cooldown_state("o/r") is None

    def test_redispatch_timing_uses_provider_cooldown_and_writes_outputs(self, tmp_path, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(
                os.environ,
                {
                    "GITHUB_OUTPUT": str(github_output),
                    "REPO_VARIABLE_WRITER_PAT": "writer",
                },
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._provider_cooldown",
                return_value=(
                    "github:SPECKIT_PR_TOKEN",
                    CooldownRecord(resume_at=now.timestamp() + 180, source="retry-after", updated_at=100),
                ),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            mock_gh_api.return_value = json.dumps(
                {
                    "workflow_runs": [
                        {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T09:59:50Z"}
                    ]
                }
            )

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["sleep_seconds"] == 180
        assert payload["throttle_reason"] == "provider_cooldown"
        assert payload["cooldown_key"] == "github:SPECKIT_PR_TOKEN"
        assert mock_gh_api.call_count == 1
        assert mock_gh_api.call_args.kwargs["token"] == "writer"
        assert github_output.read_text(encoding="utf-8").splitlines() == ["should_dispatch=true", "sleep_seconds=180"]

    def test_redispatch_recheck_blocks_dispatch_when_cooldown_still_active(self, tmp_path, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-recheck",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._provider_cooldown",
                return_value=(
                    "github:SPECKIT_PR_TOKEN",
                    CooldownRecord(resume_at=now.timestamp() + 30, source="fallback", updated_at=100),
                ),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        assert payload["decision"] == "defer_to_watchdog"
        assert github_output.read_text(encoding="utf-8").strip() == "should_dispatch=false"

    def test_redispatch_wait_rechecks_after_bounded_sleep(self, tmp_path, capsys) -> None:
        github_output = tmp_path / "github-output.txt"
        timing_outputs = [
            {"should_dispatch": True, "sleep_seconds": 120},
            {"should_dispatch": False, "sleep_seconds": -1},
        ]
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-wait",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._calculate_redispatch_timing",
                side_effect=timing_outputs,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.time.sleep") as mock_sleep,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        assert payload["sleep_seconds"] == 0
        mock_sleep.assert_called_once_with(60)
        assert github_output.read_text(encoding="utf-8").splitlines() == [
            "should_dispatch=false",
            "sleep_seconds=0",
        ]

    def test_redispatch_wait_returns_without_sleep_when_not_dispatchable(self, tmp_path, capsys) -> None:
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-wait",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._calculate_redispatch_timing",
                return_value={"should_dispatch": False, "sleep_seconds": 0},
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.time.sleep") as mock_sleep,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        assert payload["sleep_seconds"] == 0
        mock_sleep.assert_not_called()
        assert github_output.read_text(encoding="utf-8").splitlines() == [
            "should_dispatch=false",
            "sleep_seconds=0",
        ]

    def test_redispatch_wait_defers_when_cooldown_exceeds_budget(self, tmp_path, capsys) -> None:
        github_output = tmp_path / "github-output.txt"
        # First timing call fits within budget; second recheck extends beyond remaining budget.
        timing_outputs = [
            {"should_dispatch": True, "sleep_seconds": 100, "decision": "dispatch", "throttle_reason": "cooldown"},
            {
                "should_dispatch": True,
                "sleep_seconds": 260,
                "decision": "dispatch",
                "throttle_reason": "provider_cooldown",
            },
        ]
        # Monotonic: call_start=1000, first budget check after 10s elapsed (budget_left=290 > 100),
        # second budget check after 70s elapsed (budget_left=230 < 260 → defer).
        monotonic_values = [1000.0, 1010.0, 1070.0]
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-wait",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._calculate_redispatch_timing",
                side_effect=timing_outputs,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.time.sleep") as mock_sleep,
            patch("agentic_devtools.cli.ci.watchdog_command.time.monotonic", side_effect=monotonic_values),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        assert payload["decision"] == "defer_to_watchdog"
        assert payload["sleep_seconds"] == 0
        mock_sleep.assert_called_once_with(60)
        assert github_output.read_text(encoding="utf-8").splitlines() == [
            "should_dispatch=false",
            "sleep_seconds=0",
        ]

    def test_redispatch_timing_skips_when_throttler_is_in_progress(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {"workflow_runs": [{"status": "in_progress", "updated_at": "2026-07-27T09:59:50Z"}]}
                ),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        assert payload["throttle_reason"] == "in_progress"

    def test_redispatch_timing_defers_to_watchdog_beyond_horizon(self, tmp_path, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._provider_cooldown",
                return_value=(
                    "github:SPECKIT_PR_TOKEN",
                    CooldownRecord(resume_at=now.timestamp() + 301, source="retry-after", updated_at=100),
                ),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value=json.dumps({"workflow_runs": []})),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        assert payload["decision"] == "defer_to_watchdog"
        assert github_output.read_text(encoding="utf-8").splitlines() == ["should_dispatch=false", "sleep_seconds=0"]

    def test_redispatch_timing_reports_failed_last_run_without_waiting(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "failure", "updated_at": "2026-07-27T09:59:50Z"}
                        ]
                    }
                ),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["sleep_seconds"] == 0
        assert payload["throttle_reason"] == "last_run_not_success"

    def test_redispatch_timing_defers_throttler_read_until_cooldown_expires(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._provider_cooldown",
                return_value=(
                    "github:SPECKIT_PR_TOKEN",
                    CooldownRecord(resume_at=now.timestamp() + 10, updated_at=100),
                ),
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T09:59:10Z"}
                        ]
                    }
                ),
            ) as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["sleep_seconds"] == 10
        assert payload["throttle_reason"] == "provider_cooldown"
        mock_gh_api.assert_not_called()

    def test_redispatch_timing_keeps_throttler_wait_when_writer_token_available(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"REPO_VARIABLE_WRITER_PAT": "writer-token"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._provider_cooldown",
                return_value=(
                    "github:SPECKIT_PR_TOKEN",
                    CooldownRecord(resume_at=now.timestamp() + 10, updated_at=100),
                ),
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T09:59:10Z"}
                        ]
                    }
                ),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["sleep_seconds"] == 15
        assert payload["throttle_reason"] == "cooldown"

    def test_redispatch_timing_resolves_default_branch_when_not_provided(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 0, tzinfo=UTC)
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                ],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                side_effect=[
                    json.dumps({"default_branch": "main"}),
                    json.dumps({"workflow_runs": []}),
                ],
            ) as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["sleep_seconds"] == 0
        assert payload["throttle_reason"] == "no_prior_run"
        assert mock_gh_api.call_count == 2

    def test_redispatch_timing_treats_invalid_timestamp_as_no_prior_run(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-timing",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {"workflow_runs": [{"status": "completed", "conclusion": "success", "updated_at": "bad"}]}
                ),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["sleep_seconds"] == 0
        assert payload["throttle_reason"] == "no_prior_run"

    def test_redispatch_recheck_allows_dispatch_without_active_cooldown(self, tmp_path, capsys) -> None:
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-recheck",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps({"workflow_runs": []}),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["decision"] == "dispatch"
        assert github_output.read_text(encoding="utf-8").strip() == "should_dispatch=true"

    def test_redispatch_recheck_handles_output_write_error(self, capsys) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-recheck",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": "/tmp/blocked"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps({"workflow_runs": []}),
            ),
            patch("builtins.open", side_effect=OSError("blocked")),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True

    def test_redispatch_recheck_resolves_default_branch_when_not_provided(self, tmp_path, capsys) -> None:
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-recheck",
                    "--repo",
                    "o/r",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                side_effect=[
                    json.dumps({"default_branch": "main"}),
                    json.dumps({"workflow_runs": []}),
                ],
            ) as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["throttle_reason"] == "no_prior_run"
        assert github_output.read_text(encoding="utf-8").strip() == "should_dispatch=true"
        assert mock_gh_api.call_count == 2

    def test_redispatch_recheck_blocks_dispatch_when_throttler_ran_during_sleep(self, tmp_path, capsys) -> None:
        github_output = tmp_path / "github-output.txt"
        with (
            patch.object(
                sys,
                "argv",
                [
                    "agdt-ai-pr-loop-watchdog",
                    "--mode",
                    "redispatch-recheck",
                    "--repo",
                    "o/r",
                    "--default-branch",
                    "main",
                ],
            ),
            patch.dict(os.environ, {"GITHUB_OUTPUT": str(github_output)}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "in_progress", "conclusion": None, "updated_at": "2026-07-27T10:00:00Z"}
                        ]
                    }
                ),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        assert payload["decision"] == "defer_to_watchdog"
        assert payload["throttle_reason"] == "in_progress"
        assert github_output.read_text(encoding="utf-8").strip() == "should_dispatch=false"

    def test_rate_limit_error_during_provider_phase_emits_pause_output(self, capsys) -> None:
        """ProviderRateLimitError from list_eligible_prs persists cooldown and emits rate_limit_paused."""
        from datetime import UTC, datetime

        from agentic_devtools.cli.ci.cooldown import CooldownRecord
        from agentic_devtools.cli.ci.retry import ProviderRateLimitError

        now = datetime(2026, 7, 27, 10, 5, 0, tzinfo=UTC)
        resume_ts = now.timestamp() + 3600
        exc = ProviderRateLimitError(
            retry_after_seconds=3600,
            reset_timestamp=resume_ts,
            provider="github",
            credential_identity="COPILOT_GITHUB_TOKEN",
            source="dispatch-stderr",
        )
        record = CooldownRecord(
            resume_at=resume_ts,
            reason="rate_limit",
            source="dispatch-stderr",
            updated_at=now.timestamp(),
        )
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r", "--default-branch", "main"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T10:00:00Z"}
                        ]
                    }
                ),
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.persist_cooldown",
                return_value=("github:COPILOT_GITHUB_TOKEN", record),
            ),
        ):
            mock_provider_cls.return_value.list_eligible_prs.side_effect = exc

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "rate_limit_paused"
        assert payload["cooldown_source"] == "dispatch-stderr"
        assert payload["dispatched"] is False
        assert payload["eligible_count"] is None

    def test_rate_limit_error_without_persisted_cooldown_still_emits_pause_output(self, capsys) -> None:
        """ProviderRateLimitError with persist_cooldown returning None uses exc attributes directly."""
        from datetime import UTC, datetime

        from agentic_devtools.cli.ci.retry import ProviderRateLimitError

        now = datetime(2026, 7, 27, 10, 5, 0, tzinfo=UTC)
        exc = ProviderRateLimitError(
            provider="github",
            credential_identity="COPILOT_GITHUB_TOKEN",
            source="dispatch-stderr",
        )
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r", "--default-branch", "main"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps(
                    {
                        "workflow_runs": [
                            {"status": "completed", "conclusion": "success", "updated_at": "2026-07-27T10:00:00Z"}
                        ]
                    }
                ),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.persist_cooldown", return_value=None),
        ):
            mock_provider_cls.return_value.list_eligible_prs.side_effect = exc

            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "rate_limit_paused"
        assert payload["cooldown_key"] == ""
        assert payload["cooldown_source"] == "dispatch-stderr"
        assert payload["dispatched"] is False

    def test_retryable_rate_limit_is_normalized_and_paused(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 5, 0, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
            patch("agentic_devtools.cli.ci.watchdog_command.persist_cooldown", return_value=None),
        ):
            mock_gh_api.side_effect = RetryableError(
                "rate limited",
                retry_after=120,
                provider="github",
                credential_identity="COPILOT_GITHUB_TOKEN",
                source="retry-after",
                is_rate_limit=True,
            )
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "rate_limit_paused"
        assert payload["cooldown_source"] == "retry-after"

    def test_retryable_rate_limit_with_persisted_record_uses_record_source(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 5, 0, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                side_effect=RetryableError("rate limited", retry_after=120, source="retry-after", is_rate_limit=True),
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.persist_cooldown",
                return_value=(
                    "github:COPILOT_GITHUB_TOKEN",
                    CooldownRecord(resume_at=now.timestamp() + 10, source="fallback"),
                ),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["cooldown_key"] == "github:COPILOT_GITHUB_TOKEN"
        assert payload["cooldown_source"] == "fallback"

    def test_non_rate_limit_provider_error_exits_failure(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._cooldown_availability", return_value=(True, "available")),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                return_value=json.dumps({"default_branch": "main"}),
            ),
        ):
            mock_provider_cls.return_value.list_eligible_prs.side_effect = ProviderRateLimitError(is_rate_limit=False)
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            with pytest.raises(SystemExit) as exc_info:
                ai_pr_loop_watchdog_command()

        assert exc_info.value.code == 1

    def test_non_rate_limit_retryable_error_exits_failure(self) -> None:
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                side_effect=RetryableError("server error", is_rate_limit=False),
            ),
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            with pytest.raises(SystemExit) as exc_info:
                ai_pr_loop_watchdog_command()

        assert exc_info.value.code == 1

    def test_due_probe_only_mode_skips_scheduler_dispatch_work(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-ai-pr-loop-watchdog", "--mode", "due-probe-only", "--repo", "o/r", "--default-branch", "main"],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command._get_latest_throttler_run", return_value=None),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._load_cooldown_state",
                return_value=CooldownState("gh", "cred1", "generation-1", now),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=1),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "due_probe_only"
        assert payload["due_probe_count"] == 1
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()
        mock_gh_api.assert_not_called()

    def test_due_probe_only_mode_seeds_from_active_cooldown(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        with (
            patch.object(sys, "argv", ["agdt-ai-pr-loop-watchdog", "--mode", "due-probe-only", "--repo", "o/r"]),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider") as mock_provider_cls,
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._provider_cooldown",
                return_value=("github:GH_TOKEN", CooldownRecord(resume_at=now.timestamp() + 60, source="fallback")),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=2) as mock_due_probes,
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["decision"] == "due_probe_only"
        assert payload["cooldown_active"] is True
        assert payload["due_probe_count"] == 2
        cooldown_state = mock_due_probes.call_args.kwargs["cooldown_state"]
        assert cooldown_state.credential_identity == "GH_TOKEN"
        mock_gh_api.assert_not_called()
        mock_provider_cls.return_value.list_eligible_prs.assert_not_called()

    def test_due_probe_only_mode_handles_zero_due_count_without_notice(self, capsys) -> None:
        now = datetime(2026, 7, 27, 10, 0, 30, tzinfo=UTC)
        with (
            patch.object(
                sys,
                "argv",
                ["agdt-ai-pr-loop-watchdog", "--mode", "due-probe-only", "--repo", "o/r", "--default-branch", "main"],
            ),
            patch.dict(os.environ, {}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command.shutil.which", return_value="/usr/bin/gh"),
            patch("agentic_devtools.cli.ci.watchdog_command.resolve_github_repo", return_value="o/r"),
            patch("agentic_devtools.cli.ci.watchdog_command.GitHubActionsProvider"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._provider_cooldown", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command._get_latest_throttler_run", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command._load_cooldown_state", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command._seed_cooldown_state", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command.run_due_probe_wakeup", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api") as mock_gh_api,
        ):
            from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command

            ai_pr_loop_watchdog_command()

        out = capsys.readouterr().out
        payload = json.loads(out.splitlines()[-1])
        assert payload["decision"] == "due_probe_only"
        assert payload["due_probe_count"] == 0
        assert "::notice::ai-pr-loop-watchdog evaluated" not in out
        mock_gh_api.assert_not_called()
