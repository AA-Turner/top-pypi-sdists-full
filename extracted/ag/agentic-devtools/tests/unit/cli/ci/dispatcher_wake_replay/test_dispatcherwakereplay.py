"""Guarded replay of durable dispatcher wake-ups."""

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
NO_WORK_OUTCOME = dict(decision="no_eligible_prs", eligible_count=0, throttled=False, availability_established=True)
MODULE = "agentic_devtools.cli.ci.dispatcher_wake_replay"


@pytest.fixture
def harness():
    provider = Mock()
    provider.list_eligible_prs.return_value = [Mock(number=42)]
    store = Mock()
    store.entries.return_value = {"wake": ENTRY.copy()}
    store.acknowledge.return_value = True
    store.postpone.return_value = True
    with (
        patch(f"{MODULE}.time.time", return_value=100.0),
        patch(f"{MODULE}._gh_api", return_value=json.dumps(PR)) as api,
        patch(f"{MODULE}.require_default_repo_workflow_token", return_value="default"),
        patch(f"{MODULE}._provider_cooldown", return_value=None) as cooldown,
        patch(f"{MODULE}._reconcile_due_probes_and_check_availability", return_value=(0, True, "available")),
        patch(
            f"{MODULE}.persist_cooldown",
            return_value=("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", Mock(resume_at=1000.0)),
        ),
        patch(f"{MODULE}.is_copilot_session_active_via_agent_task", return_value=False) as session,
        patch(f"{MODULE}.DispatcherThrottle") as throttle,
    ):
        throttle.return_value._lookup_last_run.return_value = {}
        throttle.return_value._is_throttled.return_value = False
        yield replay.DispatcherWakeReplay(provider, store), store, api, cooldown, session, throttle


@pytest.mark.parametrize(
    ("live_pr", "eligible"),
    [(PR, True), ({**PR, "draft": True, "title": "[WIP] Finished change"}, True), (PR, False)],
)
def test_due_entry_rechecks_head_task_throttle_and_posts_once(harness, live_pr, eligible):
    runner, store, api, _, session, throttle = harness
    api.return_value = json.dumps(live_pr)
    runner.provider.list_eligible_prs.return_value = [Mock(number=42)] if eligible else []
    assert runner.run(REPO, "main") is eligible
    session.assert_called_once_with(REPO, 42, head_branch="branch", pr_id=123, head_sha=SHA, provider=runner.provider)
    throttle.assert_called_once_with(max_attempts=1, retry_window_seconds=0)
    if eligible:
        assert api.call_args_list[-1].kwargs == {"method": "POST", "body": {"ref": "main"}, "token": "default"}
        assert api.call_args_list[-1].args == (f"/repos/{REPO}/actions/workflows/ai-pr-loop-throttler.yml/dispatches",)
        store.acknowledge.assert_called_once_with("wake", ENTRY)
    else:
        store.acknowledge.assert_not_called()


def test_future_deadline_survives_restart_until_due(harness):
    runner, store, api, _, _, _ = harness
    store.entries.return_value = {"wake": {**ENTRY, "resume_at": 101.0}}
    assert runner.run(REPO, "main") is False
    api.assert_not_called()
    store.acknowledge.assert_not_called()
    with patch(f"{MODULE}.time.time", return_value=102.0):
        assert replay.DispatcherWakeReplay(runner.provider, store).run(REPO, "main")
    assert api.call_args.kwargs["method"] == "POST"


@pytest.mark.parametrize("entries", [{}, {"wake": {**ENTRY, "status": "delivered"}}])
def test_no_pending_wakes_does_not_replace_normal_watchdog(harness, entries):
    runner, store, api, _, _, _ = harness
    store.entries.return_value = entries
    assert runner.run(REPO, "main") is False
    api.assert_not_called()


def test_unavailable_independent_store_falls_back_without_delivery_claim(harness, caplog):
    runner, store, api, _, _, _ = harness
    store.entries.side_effect = RuntimeError("writer unavailable")
    assert runner.run(REPO, "main") is False
    api.assert_not_called()
    store.acknowledge.assert_not_called()
    assert "unavailable" in caplog.text


def test_default_store_uses_the_existing_provider(harness):
    runner, _, _, _, _, _ = harness
    with patch(f"{MODULE}.DispatcherWakeStore") as store:
        replay.DispatcherWakeReplay(runner.provider)
    store.assert_called_once_with(runner.provider)


@pytest.mark.parametrize("state,head", [("closed", SHA), ("open", "b" * 40)])
def test_stale_or_closed_wake_is_retired_without_dispatch(harness, state, head):
    runner, store, api, _, _, _ = harness
    api.return_value = json.dumps({**PR, "state": state, "head": {"sha": head}})
    assert runner.run(REPO, "main") is False
    assert api.call_count == 1
    store.acknowledge.assert_called_once_with("wake", ENTRY)


def test_failed_obsolete_retirement_is_visible(harness, caplog):
    runner, store, api, _, _, _ = harness
    api.return_value = json.dumps({**PR, "state": "closed"})
    store.acknowledge.return_value = False
    assert runner.run(REPO, "main") is False
    assert "retirement is unconfirmed" in caplog.text


@pytest.mark.parametrize("active", [True, None])
def test_active_or_unknown_task_preserves_pending_intent(harness, active):
    runner, store, api, _, session, _ = harness
    session.return_value = active
    assert runner.run(REPO, "main") is False
    assert api.call_count == 1
    store.acknowledge.assert_not_called()


@pytest.mark.parametrize("failure_stage", ["live_pr_read", "throttle_lookup"])
def test_pre_post_provider_failure_stops_replay_and_fails_closed(harness, failure_stage, capsys):
    runner, store, api, _, _, throttle = harness
    store.entries.return_value = {
        "wake": ENTRY,
        "second": {**ENTRY, "event": "pull_request_target:labeled"},
    }
    error = RuntimeError("HTTP 403 Forbidden")
    if failure_stage == "live_pr_read":
        api.side_effect = error
    else:
        throttle.return_value._lookup_last_run.side_effect = error

    assert runner.run(REPO, "main") is False

    assert runner.dispatch_failed is True
    assert store.entries.return_value["wake"]["status"] == "pending"
    store.acknowledge.assert_not_called()
    assert api.call_count == 1
    assert "PR 42" in capsys.readouterr().out


@pytest.mark.parametrize("last_run", [{"status": "in_progress"}, {"updated_at": "recent"}])
def test_active_throttler_or_cooldown_does_not_acknowledge(harness, last_run):
    runner, store, api, _, _, throttle = harness
    throttle.return_value._lookup_last_run.return_value = last_run
    throttle.return_value._is_throttled.return_value = True
    assert runner.run(REPO, "main") is False
    assert api.call_count == 1
    store.acknowledge.assert_not_called()


def test_independent_provider_cooldown_defers_before_default_api(harness):
    runner, store, api, cooldown, _, _ = harness
    cooldown.return_value = ("github:default", Mock(resume_at=600.0))
    assert runner.run(REPO, "main") is False
    store.postpone.assert_called_once_with("wake", ENTRY, 600.0)
    api.assert_not_called()
    assert cooldown.call_args.args == (runner.provider, cooldown.call_args.args[1])


@pytest.mark.parametrize(
    "error",
    [
        ProviderRateLimitError(reset_timestamp=900),
        RetryableError("secondary", retry_after=500, is_rate_limit=True),
        RuntimeError("permission denied HTTP 403"),
        RetryableError("HTTP 502", is_rate_limit=False),
        RuntimeError("opaque provider response"),
    ],
)
def test_failed_post_keeps_pending_and_honors_renewed_provider_deadline(harness, error, capsys):
    runner, store, api, _, _, _ = harness
    api.side_effect = [json.dumps(PR), json.dumps(PR), error]
    assert runner.run(REPO, "main") is True
    store.acknowledge.assert_not_called()
    if isinstance(error, (ProviderRateLimitError, RetryableError)) and error.is_rate_limit:
        assert store.postpone.call_args.args[2] >= 600.0
    else:
        store.postpone.assert_not_called()
        assert runner.dispatch_failed is True
        diagnostic = capsys.readouterr().out
        assert "PR 42" in diagnostic and SHA in diagnostic and ENTRY["event"] in diagnostic


def test_failed_deadline_write_retains_pending_after_failed_post(harness, caplog):
    runner, store, api, _, _, _ = harness
    api.side_effect = [json.dumps(PR), json.dumps(PR), ProviderRateLimitError(retry_after_seconds=500)]
    store.postpone.side_effect = RuntimeError("writer unavailable")
    assert runner.run(REPO, "main")
    store.acknowledge.assert_not_called()
    assert "Could not persist dispatcher wake deadline" in caplog.text


def test_unconfirmed_shared_cooldown_write_keeps_wake_pending(harness, caplog):
    runner, store, api, _, _, _ = harness
    rate_limit = ProviderRateLimitError(retry_after_seconds=500)
    api.side_effect = [json.dumps(PR), json.dumps(PR), rate_limit]
    with patch(f"{MODULE}.persist_cooldown", return_value=None) as persist:
        assert runner.run(REPO, "main") is True

    persisted_error = persist.call_args.args[1]
    assert persisted_error.reset_timestamp == 600.0
    assert persisted_error.remaining == 0
    assert persist.call_args.kwargs["now"] == 100.0
    store.postpone.assert_called_once()
    store.acknowledge.assert_not_called()
    assert "Shared provider cooldown persistence unconfirmed" in caplog.text
    assert "42" in caplog.text and SHA in caplog.text and ENTRY["event"] in caplog.text


def test_unconfirmed_shared_and_wake_deadlines_blocks_fallback(harness, capsys):
    runner, store, api, _, _, _ = harness
    api.side_effect = [json.dumps(PR), json.dumps(PR), ProviderRateLimitError(retry_after_seconds=500)]
    store.postpone.return_value = False
    with patch(f"{MODULE}.persist_cooldown", return_value=None):
        assert runner.run(REPO, "main") is True

    assert runner.persistence_unconfirmed is True
    store.acknowledge.assert_not_called()
    assert "no confirmed shared or per-wake deadline" in capsys.readouterr().out


def test_short_shared_deadline_does_not_count_when_wake_postponement_fails(harness, caplog):
    runner, store, api, _, _, _ = harness
    error = ProviderRateLimitError(retry_after_seconds=60, reset_timestamp=900, remaining=0)
    api.side_effect = [json.dumps(PR), json.dumps(PR), error]
    store.postpone.return_value = False
    with patch(
        f"{MODULE}.persist_cooldown",
        return_value=("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", Mock(resume_at=170.0)),
    ) as persist:
        assert runner.run(REPO, "main") is True

    persisted_error = persist.call_args.args[1]
    assert persisted_error.reset_timestamp == 900.0
    assert runner.persistence_unconfirmed is True
    store.acknowledge.assert_not_called()
    assert "Shared provider cooldown persistence unconfirmed or shorter" in caplog.text


def test_full_shared_deadline_survives_restart_when_wake_postponement_fails(harness):
    runner, store, api, cooldown, _, _ = harness
    error = ProviderRateLimitError(retry_after_seconds=60, reset_timestamp=900, remaining=0)
    api.side_effect = [json.dumps(PR), json.dumps(PR), error]
    store.postpone.return_value = False
    with patch(
        f"{MODULE}.persist_cooldown",
        return_value=("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", Mock(resume_at=900.0)),
    ):
        assert runner.run(REPO, "main") is True

    assert runner.persistence_unconfirmed is False
    store.acknowledge.assert_not_called()
    store.postpone.return_value = True
    cooldown.return_value = ("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", Mock(resume_at=900.0))
    with patch(f"{MODULE}.time.time", return_value=200.0):
        assert replay.DispatcherWakeReplay(runner.provider, store).run(REPO, "main") is False
    cooldown.assert_called()
    assert api.call_count == 3
    store.acknowledge.assert_not_called()


def test_deadline_derivation_failure_blocks_fallback(harness, caplog):
    runner, store, api, _, _, _ = harness
    api.side_effect = [json.dumps(PR), json.dumps(PR), ProviderRateLimitError(retry_after_seconds=500)]
    with patch(f"{MODULE}.wake_resume_at", side_effect=RuntimeError("deadline unavailable")):
        assert runner.run(REPO, "main") is True

    assert runner.persistence_unconfirmed is True
    store.postpone.assert_not_called()
    store.acknowledge.assert_not_called()
    assert "Could not derive shared dispatcher deadline" in caplog.text


def test_shared_deadline_write_exception_falls_back_to_confirmed_wake_deadline(harness, caplog):
    runner, store, api, _, _, _ = harness
    api.side_effect = [json.dumps(PR), json.dumps(PR), ProviderRateLimitError(retry_after_seconds=500)]
    with patch(f"{MODULE}.persist_cooldown", side_effect=RuntimeError("writer unavailable")):
        assert runner.run(REPO, "main") is True

    assert runner.persistence_unconfirmed is False
    store.postpone.assert_called_once()
    assert "Could not persist shared provider cooldown" in caplog.text


def test_unconfirmed_provider_cooldown_deferral_keeps_intent_pending(harness, caplog):
    runner, store, api, cooldown, _, _ = harness
    cooldown.return_value = ("github:default", Mock(resume_at=600.0))
    store.postpone.return_value = False

    assert runner.run(REPO, "main") is False

    assert "Provider cooldown deferral unconfirmed" in caplog.text
    store.acknowledge.assert_not_called()
    api.assert_not_called()


def test_false_postponement_warns_and_next_tick_rechecks_live_guards(harness, caplog):
    runner, store, api, cooldown, _, throttle = harness
    api.side_effect = [json.dumps(PR), json.dumps(PR), ProviderRateLimitError(retry_after_seconds=500)]
    store.postpone.return_value = False
    assert runner.run(REPO, "main") is True
    assert "deadline persistence unconfirmed" in caplog.text
    for identity in ("42", SHA, ENTRY["event"]):
        assert identity in caplog.text
    store.acknowledge.assert_not_called()
    assert store.entries.return_value["wake"] == ENTRY
    assert ENTRY["status"] == "pending"

    api.reset_mock()
    api.side_effect = None
    cooldown.reset_mock()
    throttle.reset_mock()
    throttle.return_value._is_throttled.return_value = True
    assert replay.DispatcherWakeReplay(runner.provider, store).run(REPO, "main") is False
    cooldown.assert_called_once()
    api.assert_called_once_with(f"/repos/{REPO}/pulls/42", token="default")
    throttle.return_value._lookup_last_run.assert_called_once_with(REPO, "main")
    throttle.return_value._is_throttled.assert_called_once()
    store.acknowledge.assert_not_called()


@pytest.mark.parametrize(
    ("available", "reason"),
    [(False, "cooldown_pending"), (False, "cooldown_state_unknown")],
)
def test_due_probe_availability_gate_blocks_replay_dispatch(harness, available, reason, caplog):
    runner, store, api, _, _, _ = harness
    with patch(
        f"{MODULE}._reconcile_due_probes_and_check_availability",
        return_value=(0, available, reason),
    ) as gate:
        assert runner.run(REPO, "main") is False
    gate.assert_called_once()
    assert "blocked by watchdog availability gate" in caplog.text
    assert reason in caplog.text
    assert api.call_count == 1
    store.acknowledge.assert_not_called()


def test_closed_event_preserves_scheduler_intent_for_repository_discovery(harness):
    runner, store, api, _, _, _ = harness
    closed_entry = {**ENTRY, "event": "pull_request_target:closed:123"}
    store.entries.return_value = {"closed": closed_entry}
    api.return_value = json.dumps({**PR, "state": "closed"})
    assert runner.run(REPO, "main") is False
    assert runner.scheduler_wake_required is True
    store.acknowledge.assert_not_called()
    assert api.call_count == 1


@pytest.mark.parametrize(
    ("outcome", "acknowledged"),
    [
        ({"dispatched": True, "availability_established": True}, True),
        (NO_WORK_OUTCOME, True),
        ({"dispatched": False, "availability_established": False}, False),
        ({"decision": "throttled", "dispatched": False, "availability_established": True}, False),
        (None, False),
    ],
)
def test_closed_event_is_acknowledged_only_after_confirmed_scheduler_outcome(harness, outcome, acknowledged):
    runner, store, api, _, _, _ = harness
    closed_entry = {**ENTRY, "event": "pull_request_target:closed:123"}
    store.entries.return_value = {"closed": closed_entry}
    api.return_value = json.dumps({**PR, "state": "closed"})
    assert runner.run(REPO, "main") is False

    runner.acknowledge_scheduler_handoff(outcome)

    assert (store.acknowledge.call_count == 1) is acknowledged
    if acknowledged:
        store.acknowledge.assert_called_once_with("closed", closed_entry)


def test_scheduler_outcome_without_closed_wake_does_not_acknowledge(harness):
    runner, store, _, _, _, _ = harness
    runner.acknowledge_scheduler_handoff({"dispatched": True, "availability_established": True})
    store.acknowledge.assert_not_called()


def test_unconfirmed_closed_event_handoff_acknowledgment_is_visible(harness, caplog):
    runner, store, api, _, _, _ = harness
    closed_entry = {**ENTRY, "event": "pull_request_target:closed:123"}
    store.entries.return_value = {"closed": closed_entry}
    store.acknowledge.return_value = False
    api.return_value = json.dumps({**PR, "state": "closed"})
    assert runner.run(REPO, "main") is False

    runner.acknowledge_scheduler_handoff({"dispatched": True, "availability_established": True})

    store.acknowledge.assert_called_once_with("closed", closed_entry)
    assert "acknowledgment unconfirmed" in caplog.text


def test_rotating_bounded_batch_reaches_sixth_wake_on_next_tick(harness):
    runner, store, api, _, session, _ = harness
    entries = {
        str(number): {**ENTRY, "pr_number": number, "event": f"pull_request_target:synchronize:{number}"}
        for number in range(1, 7)
    }
    store.entries.return_value = entries
    runner.provider.list_eligible_prs.return_value = [Mock(number=number) for number in range(1, 7)]
    session.side_effect = lambda repository, pr_number, **kwargs: pr_number != 6
    with patch(f"{MODULE}.time.time", return_value=102.0):
        with patch.dict("os.environ", {"GITHUB_RUN_ID": "102"}):
            assert runner.run(REPO, "main") is False
            assert api.call_count == 5
        with patch.dict("os.environ", {"GITHUB_RUN_ID": "103"}):
            assert runner.run(REPO, "main") is True
    assert api.call_count == 12
    assert store.acknowledge.call_count == 1


def test_invalid_run_id_uses_clock_for_batch_rotation(harness):
    runner, store, api, _, _, _ = harness
    store.entries.return_value = {"wake": ENTRY}
    with patch(f"{MODULE}.time.time", return_value=100.0), patch.dict("os.environ", {"GITHUB_RUN_ID": "invalid"}):
        assert runner.run(REPO, "main") is True
    assert api.call_count == 3
    assert store.acknowledge.call_count == 1


def test_rate_limit_before_post_defers_without_an_attempt(harness):
    runner, store, api, _, _, throttle = harness
    throttle.return_value._lookup_last_run.side_effect = [
        ProviderRateLimitError(reset_timestamp=900),
        RetryableError("temporary provider error"),
    ]
    assert runner.run(REPO, "main") is False
    assert api.call_count == 1
    assert runner.run(REPO, "main") is False
    assert store.postpone.call_count == 1


def test_failed_ack_does_not_claim_delivery_and_next_run_rechecks_throttle(harness, caplog):
    runner, store, api, _, _, throttle = harness
    store.acknowledge.return_value = False
    assert runner.run(REPO, "main") is True
    assert "unconfirmed" in caplog.text
    throttle.return_value._is_throttled.return_value = True
    api.reset_mock()
    assert runner.run(REPO, "main") is False
    assert api.call_count == 1


def test_concurrent_ack_or_change_prevents_post(harness):
    runner, store, api, _, _, _ = harness
    store.entries.side_effect = [{"wake": ENTRY}, {}]
    assert runner.run(REPO, "main") is False
    assert api.call_count == 1
    store.acknowledge.assert_not_called()


def test_one_successful_post_per_invocation_for_many_due_entries(harness):
    runner, store, api, _, _, _ = harness
    store.entries.return_value = {"wake": ENTRY, "second": {**ENTRY, "event": "pull_request_target:labeled"}}
    assert runner.run(REPO, "main") is True
    assert api.call_count == 3
    assert store.acknowledge.call_count == 1


def test_unknown_post_outcome_does_not_attempt_another_entry_in_the_same_invocation(harness):
    runner, store, api, _, _, _ = harness
    store.entries.return_value = {"wake": ENTRY, "second": {**ENTRY, "event": "pull_request_target:labeled"}}
    api.side_effect = [json.dumps(PR), json.dumps(PR), RuntimeError("response lost")]
    assert runner.run(REPO, "main")
    assert api.call_count == 3
    store.acknowledge.assert_not_called()


def test_head_changed_during_inventory_is_retired_before_post(harness):
    runner, store, api, _, _, _ = harness
    api.side_effect = [json.dumps(PR), json.dumps({**PR, "head": {"sha": "b" * 40}})]
    assert runner.run(REPO, "main") is False
    assert api.call_count == 2
    store.acknowledge.assert_called_once_with("wake", ENTRY)


@pytest.mark.parametrize(
    "pr",
    [[], {}, {**PR, "head": None}, {**PR, "head": {"sha": SHA}}, {**PR, "head": {"sha": SHA, "ref": ""}}],
)
def test_malformed_live_response_fails_closed(harness, pr):
    runner, store, api, _, _, _ = harness
    api.return_value = json.dumps(pr)
    assert runner.run(REPO, "main") is False
    store.acknowledge.assert_not_called()
    assert api.call_count == 1
