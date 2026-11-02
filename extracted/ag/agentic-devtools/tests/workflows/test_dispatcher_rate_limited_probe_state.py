"""Integration coverage for replay deferral after rate-limited probe-state reads."""

import json
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci import dispatcher_wake_replay as replay
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

REPO = "owner/repo"
SHA = "a" * 40
ENTRY = {
    "pr_number": 42,
    "head_sha": SHA,
    "event": "pull_request_target:synchronize",
    "resume_at": 100.0,
    "status": "pending",
}
PR = {"number": 42, "id": 123, "state": "open", "draft": False, "head": {"sha": SHA, "ref": "branch"}}
MODULE = "agentic_devtools.cli.ci.dispatcher_wake_replay"
WATCHDOG = "agentic_devtools.cli.ci.watchdog_command"


@pytest.mark.parametrize(
    "error",
    [
        ProviderRateLimitError(retry_after_seconds=500),
        RetryableError("secondary rate limit", retry_after=500, is_rate_limit=True),
    ],
)
def test_rate_limited_probe_state_read_without_shared_cooldown_postpones_wake(error):
    store = Mock()
    store.entries.return_value = {"wake": ENTRY.copy()}
    store.postpone.return_value = True
    with (
        patch(f"{MODULE}.time.time", return_value=100.0),
        patch(f"{MODULE}._gh_api", return_value=json.dumps(PR)) as api,
        patch(f"{MODULE}.require_default_repo_workflow_token", return_value="default"),
        patch(f"{MODULE}._provider_cooldown", return_value=None),
        patch(f"{MODULE}.persist_cooldown", return_value=None),
        patch(f"{MODULE}.DispatcherThrottle") as throttle,
        patch(f"{WATCHDOG}.QueueStore") as queue_store,
    ):
        throttle.return_value._lookup_last_run.return_value = {}
        throttle.return_value._is_throttled.return_value = False
        queue_store.return_value.load.side_effect = error
        runner = replay.DispatcherWakeReplay(Mock(), store)
        assert runner.run(REPO, "main") is False

    assert api.call_count == 1
    store.acknowledge.assert_not_called()
    store.postpone.assert_called_once()
    assert store.postpone.call_args.args[2] >= 600.0
    assert runner.persistence_unconfirmed is False
