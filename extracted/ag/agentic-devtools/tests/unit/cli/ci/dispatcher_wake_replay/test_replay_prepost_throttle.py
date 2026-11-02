"""A concurrent dispatcher starting during inventory must block replay's POST."""

from unittest.mock import Mock, patch

from agentic_devtools.cli.ci import dispatcher_wake_replay as subject


def test_run_starting_during_inventory_blocks_replay_post():
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:synchronize"}
    store = Mock()
    store.entries.return_value = {"wake": entry}
    runner = subject.DispatcherWakeReplay(Mock(), store)
    with (
        patch.object(subject, "_provider_cooldown", return_value=None),
        patch.object(subject, "require_default_repo_workflow_token", return_value="token"),
        patch.object(subject.DispatcherWakeReplay, "_current_pr", return_value={"number": 42}),
        patch.object(subject, "_reconcile_due_probes_and_check_availability", return_value=(0, True, "available")),
        patch.object(subject, "DispatcherThrottle") as throttle,
        patch.object(subject, "_gh_api") as api,
        patch.object(runner, "_eligible") as eligible,
    ):
        throttle.return_value._is_throttled.return_value = False

        def scan_inventory(*args):
            throttle.return_value._is_throttled.return_value = True
            return True

        eligible.side_effect = scan_inventory
        assert runner._replay("wake", entry, "owner/repo", "main") is False

    assert throttle.return_value._lookup_last_run.call_count == 2
    api.assert_not_called()
    store.acknowledge.assert_not_called()
    assert runner._post_attempted is False


def test_provider_cooldown_appearing_during_inventory_defers_before_post():
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:synchronize"}
    store = Mock()
    store.entries.return_value = {"wake": entry}
    runner = subject.DispatcherWakeReplay(Mock(), store)
    with (
        patch.object(subject, "_provider_cooldown", side_effect=[None, ("github:TOKEN", Mock(resume_at=900.0))]),
        patch.object(subject, "require_default_repo_workflow_token", return_value="token"),
        patch.object(subject.DispatcherWakeReplay, "_current_pr", return_value={"number": 42}),
        patch.object(subject, "_reconcile_due_probes_and_check_availability", return_value=(0, True, "available")),
        patch.object(subject, "DispatcherThrottle") as throttle,
        patch.object(subject, "_gh_api") as api,
        patch.object(runner, "_eligible", return_value=True),
    ):
        throttle.return_value._is_throttled.return_value = False
        assert runner._replay("wake", entry, "owner/repo", "main") is False
    api.assert_not_called()
    store.acknowledge.assert_not_called()
    store.postpone.assert_called_once_with("wake", entry, 900.0)
    assert runner.retained_wakes["wake"]["resume_at"] == 900.0
    assert runner._post_attempted is False
