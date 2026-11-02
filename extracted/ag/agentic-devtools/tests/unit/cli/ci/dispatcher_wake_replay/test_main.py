"""The existing watchdog command routes scheduled wake replay without new triggers."""

import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.dispatcher_wake_replay import main
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

MODULE = "agentic_devtools.cli.ci.dispatcher_wake_replay"


@pytest.mark.parametrize("mode", ["watchdog", "due-probe-only"])
@pytest.mark.parametrize("handled", [True, False])
def test_existing_watchdog_modes_replay_pending_entries_before_ordinary_work(mode, handled):
    with (
        patch(f"{MODULE}.sys.argv", ["watchdog", "--mode", mode, "--repo", "owner/repo", "--default-branch", "main"]),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.GitHubActionsProvider") as provider,
        patch(f"{MODULE}._handoff_throttled", return_value=False),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command") as original,
    ):
        runner.return_value.run.return_value = handled
        runner.return_value.persistence_unconfirmed = False
        main()
        runner.return_value.run.assert_called_once_with("owner/repo", "main")
        provider.assert_called_once_with(repo="owner/repo")
        assert original.call_count == (0 if handled else 1)


def test_unrelated_command_modes_are_unchanged():
    with (
        patch(f"{MODULE}.sys.argv", ["watchdog", "--mode", "cooldown-gate"]),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.ai_pr_loop_watchdog_command") as original,
    ):
        main()
        runner.assert_not_called()
        original.assert_called_once_with()


@pytest.mark.parametrize("extra", ["--help", "-h", "--unsupported"])
def test_help_or_unknown_arguments_are_validated_before_any_replay(extra):
    with (
        patch(f"{MODULE}.sys.argv", ["watchdog", "--repo", "owner/repo", "--default-branch", "main", extra]),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.ai_pr_loop_watchdog_command") as original,
    ):
        main()
        runner.assert_not_called()
        original.assert_called_once_with()


def test_default_mode_resolves_workflow_environment(monkeypatch):
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GITHUB_DEFAULT_BRANCH", "main")
    with (
        patch(f"{MODULE}.sys.argv", ["watchdog"]),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.GitHubActionsProvider"),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command"),
    ):
        runner.return_value.persistence_unconfirmed = False
        main()
        runner.return_value.run.assert_called_once_with("owner/repo", "main")


def test_missing_context_or_unavailable_replay_preserves_original_watchdog(monkeypatch):
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.delenv("GITHUB_DEFAULT_BRANCH", raising=False)
    with (
        patch(f"{MODULE}.sys.argv", ["watchdog"]),
        patch(f"{MODULE}.GitHubActionsProvider") as provider,
        patch(f"{MODULE}.ai_pr_loop_watchdog_command") as original,
    ):
        main()
        provider.assert_not_called()
        original.assert_called_once_with()
    with (
        patch(f"{MODULE}.sys.argv", ["watchdog", "--repo", "owner/repo", "--default-branch", "main"]),
        patch(f"{MODULE}.GitHubActionsProvider", side_effect=RuntimeError("unavailable")),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command") as original,
    ):
        main()
        original.assert_called_once_with()


@pytest.mark.parametrize("mode", ["watchdog", "due-probe-only"])
def test_scheduled_route_runs_full_scheduler_for_closed_event_wake(monkeypatch, mode):
    observed_argv = []

    def run_watchdog():
        observed_argv.extend(sys.argv)

    expected_argv = ["watchdog", "--mode", mode, "--repo", "owner/repo", "--default-branch", "main"]
    with (
        patch(
            f"{MODULE}.sys.argv",
            expected_argv,
        ),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.GitHubActionsProvider"),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command", side_effect=run_watchdog),
        patch(f"{MODULE}._handoff_throttled", return_value=False),
    ):
        runner.return_value.run.return_value = False
        runner.return_value.scheduler_wake_required = True
        runner.return_value.scheduler_wake = None
        runner.return_value.retained_wakes = {}
        runner.return_value.persistence_unconfirmed = False
        main()
        runner.return_value.acknowledge_scheduler_handoff.assert_called_once_with(None)

    assert observed_argv == (
        expected_argv
        if mode == "watchdog"
        else [
            "watchdog",
            "--mode",
            "watchdog",
            "--repo",
            "owner/repo",
            "--default-branch",
            "main",
        ]
    )


def test_unconfirmed_rate_limit_persistence_fails_closed_before_watchdog_fallback():
    with (
        patch(
            f"{MODULE}.sys.argv",
            ["watchdog", "--mode", "watchdog", "--repo", "owner/repo", "--default-branch", "main"],
        ),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.GitHubActionsProvider"),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command") as original,
    ):
        runner.return_value.run.return_value = True
        runner.return_value.persistence_unconfirmed = True
        with pytest.raises(SystemExit) as raised:
            main()

    assert raised.value.code == 1
    original.assert_not_called()


def test_failed_replay_post_exits_without_running_watchdog_fallback():
    with (
        patch(
            f"{MODULE}.sys.argv",
            ["watchdog", "--mode", "watchdog", "--repo", "owner/repo", "--default-branch", "main"],
        ),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.GitHubActionsProvider"),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command") as original,
    ):
        runner.return_value.run.return_value = True
        runner.return_value.persistence_unconfirmed = False
        runner.return_value.dispatch_failed = True

        with pytest.raises(SystemExit) as raised:
            main()

    assert raised.value.code == 1
    original.assert_not_called()


def test_closed_event_rate_limit_handoff_renews_wake_and_fails_if_unconfirmed():
    error = ProviderRateLimitError(reset_timestamp=900)
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:closed:123"}
    with (
        patch(
            f"{MODULE}.sys.argv",
            ["watchdog", "--mode", "watchdog", "--repo", "owner/repo", "--default-branch", "main"],
        ),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.GitHubActionsProvider"),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command", return_value={"_rate_limit_error": error}),
        patch(f"{MODULE}._handoff_throttled", return_value=False),
    ):
        runner.return_value.run.return_value = False
        runner.return_value.scheduler_wake_required = True
        runner.return_value.scheduler_wake = ("wake", entry)
        runner.return_value.retained_wakes = {}
        runner.return_value.persistence_unconfirmed = False
        runner.return_value._postpone_rate_limit.side_effect = lambda *args: setattr(
            runner.return_value, "persistence_unconfirmed", True
        )

        with pytest.raises(SystemExit) as raised:
            main()

    assert raised.value.code == 1
    runner.return_value._postpone_rate_limit.assert_called_once_with("wake", entry, error)
    runner.return_value.acknowledge_scheduler_handoff.assert_not_called()


def test_closed_event_rate_limit_handoff_retains_wake_after_confirmed_deadline():
    error = ProviderRateLimitError(reset_timestamp=900)
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:closed:123"}
    with (
        patch(
            f"{MODULE}.sys.argv",
            ["watchdog", "--mode", "watchdog", "--repo", "owner/repo", "--default-branch", "main"],
        ),
        patch(f"{MODULE}.DispatcherWakeReplay") as runner,
        patch(f"{MODULE}.GitHubActionsProvider"),
        patch(f"{MODULE}.ai_pr_loop_watchdog_command", return_value={"_rate_limit_error": error}),
        patch(f"{MODULE}._handoff_throttled", return_value=False),
    ):
        runner.return_value.run.return_value = False
        runner.return_value.scheduler_wake_required = True
        runner.return_value.scheduler_wake = ("wake", entry)
        runner.return_value.retained_wakes = {}
        runner.return_value.persistence_unconfirmed = False

        main()

    runner.return_value._postpone_rate_limit.assert_called_once_with("wake", entry, error)
    runner.return_value.acknowledge_scheduler_handoff.assert_not_called()
