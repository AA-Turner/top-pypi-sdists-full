"""Integration coverage for the real watchdog dispatch behind the handoff guard."""

import sys
from argparse import Namespace
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci import dispatcher_wake_replay as subject

WATCHDOG = "agentic_devtools.cli.ci.watchdog_command"


@pytest.mark.parametrize("throttled", [True, False])
def test_handoff_guards_actual_stalled_review_dispatch(throttled):
    store = Mock()
    runner = subject.DispatcherWakeReplay(Mock(), store)
    runner.scheduler_wake = ("wake", {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:closed"})
    args = Namespace(mode="watchdog", repo="owner/repo", default_branch="main")
    with (
        patch.object(sys, "argv", ["watchdog", "--repo", args.repo, "--default-branch", args.default_branch]),
        patch.dict("os.environ", {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "token"}, clear=True),
        patch.object(subject, "DispatcherThrottle") as throttle,
        patch(f"{WATCHDOG}.shutil.which", return_value="gh"),
        patch(f"{WATCHDOG}.resolve_github_repo", return_value=args.repo),
        patch(f"{WATCHDOG}.GitHubActionsProvider"),
        patch(f"{WATCHDOG}._provider_cooldown", return_value=None),
        patch(f"{WATCHDOG}._get_latest_throttler_run", return_value=None),
        patch(f"{WATCHDOG}._reconcile_due_probes_and_check_availability", return_value=(0, True, "available")),
        patch(f"{WATCHDOG}.find_stalled_unaddressed_reviews", return_value=[43]) as stalled,
        patch(f"{WATCHDOG}.auto_approve_waiting_runs", return_value=0),
        patch(f"{WATCHDOG}._dispatch_throttler") as dispatch,
    ):
        throttle.return_value._is_throttled.return_value = throttled
        subject._run_closed_event_scheduler_handoff(runner, args)

    assert dispatch.call_count == (0 if throttled else 1)
    assert stalled.call_count == (0 if throttled else 1)
    assert store.acknowledge.call_count == (0 if throttled else 1)
