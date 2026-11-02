"""Retained open wakes must not bypass provider deadlines through watchdog fallback."""

import json
import sys
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci import dispatcher_wake_replay as subject
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

WATCHDOG = "agentic_devtools.cli.ci.watchdog_command"
SHA = "a" * 40
ENTRY = {
    "pr_number": 42,
    "head_sha": SHA,
    "event": "pull_request_target:synchronize",
    "resume_at": 100.0,
    "status": "pending",
}
PR = {"number": 42, "state": "open", "head": {"sha": SHA, "ref": "branch"}}
ARGV = ["watchdog", "--repo", "owner/repo", "--default-branch", "main"]


@pytest.mark.parametrize("throttled", [True, False])
def test_open_wake_guards_real_stalled_review_fallback(throttled):
    store = Mock()
    store.entries.return_value = {"wake": ENTRY.copy()}
    with (
        patch.object(sys, "argv", ARGV),
        patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token"}, clear=True),
        patch.object(subject.time, "time", return_value=100.0),
        patch.object(subject, "DispatcherWakeStore", return_value=store),
        patch.object(subject, "GitHubActionsProvider"),
        patch.object(subject, "_gh_api", return_value=json.dumps(PR)),
        patch.object(subject, "_provider_cooldown", return_value=None),
        patch.object(subject, "_reconcile_due_probes_and_check_availability", return_value=(0, True, "available")),
        patch.object(subject.DispatcherWakeReplay, "_eligible", return_value=False),
        patch.object(subject, "DispatcherThrottle") as throttle,
        patch(f"{WATCHDOG}.shutil.which", return_value="gh"),
        patch(f"{WATCHDOG}.resolve_github_repo", return_value="owner/repo"),
        patch(f"{WATCHDOG}.GitHubActionsProvider"),
        patch(f"{WATCHDOG}._provider_cooldown", return_value=None),
        patch(f"{WATCHDOG}._get_latest_throttler_run", return_value=None),
        patch(f"{WATCHDOG}._reconcile_due_probes_and_check_availability", return_value=(0, True, "available")),
        patch(f"{WATCHDOG}.find_stalled_unaddressed_reviews", return_value=[43]),
        patch(f"{WATCHDOG}.auto_approve_waiting_runs", return_value=0),
        patch(f"{WATCHDOG}._dispatch_throttler") as dispatch,
    ):
        throttle.return_value._is_throttled.return_value = throttled
        subject.main()
    assert dispatch.call_count == (0 if throttled else 1)
    store.acknowledge.assert_not_called()


@pytest.mark.parametrize("confirmed", [True, False])
def test_retained_open_wake_fallback_rate_limit_survives_restart(confirmed):
    entries = {"wake": ENTRY.copy()}
    store = Mock()
    store.entries.side_effect = lambda: dict(entries)

    def postpone(key, entry, resume_at):
        if confirmed:
            entries[key] = {**entry, "resume_at": resume_at}
        return confirmed

    store.postpone.side_effect = postpone
    with (
        patch.object(sys, "argv", ARGV),
        patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token"}, clear=True),
        patch.object(subject.time, "time", return_value=100.0),
        patch.object(subject, "DispatcherWakeStore", return_value=store),
        patch.object(subject, "GitHubActionsProvider"),
        patch.object(subject, "_gh_api", return_value=json.dumps(PR)),
        patch.object(subject, "_provider_cooldown", return_value=None),
        patch.object(subject, "_reconcile_due_probes_and_check_availability", return_value=(0, True, "available")),
        patch.object(subject.DispatcherWakeReplay, "_eligible", return_value=False),
        patch.object(subject, "DispatcherThrottle") as throttle,
        patch.object(subject, "persist_cooldown", return_value=None),
        patch.object(
            subject,
            "ai_pr_loop_watchdog_command",
            return_value={"_rate_limit_error": ProviderRateLimitError(retry_after_seconds=500)},
        ) as watchdog,
    ):
        throttle.return_value._is_throttled.return_value = False
        if confirmed:
            subject.main()
            assert entries["wake"]["resume_at"] >= 600.0
            watchdog.reset_mock()
            subject.main()
            watchdog.assert_not_called()
        else:
            with pytest.raises(SystemExit):
                subject.main()
    store.acknowledge.assert_not_called()


@pytest.mark.parametrize("confirmed", [True, False])
def test_shared_provider_pause_blocks_fallback_even_when_postponement_fails(confirmed):
    store = Mock()
    store.entries.return_value = {"wake": ENTRY.copy()}
    store.postpone.return_value = confirmed
    with (
        patch.object(sys, "argv", ARGV),
        patch.object(subject.time, "time", return_value=100.0),
        patch.object(subject, "DispatcherWakeStore", return_value=store),
        patch.object(subject, "GitHubActionsProvider"),
        patch.object(subject, "_provider_cooldown", return_value=("github:TOKEN", Mock(resume_at=900.0))),
        patch.object(subject, "_handoff_throttled") as throttle,
        patch.object(subject, "ai_pr_loop_watchdog_command") as watchdog,
    ):
        subject.main()
    store.postpone.assert_called_once_with("wake", ENTRY, 900.0)
    throttle.assert_not_called()
    watchdog.assert_not_called()
    store.acknowledge.assert_not_called()
