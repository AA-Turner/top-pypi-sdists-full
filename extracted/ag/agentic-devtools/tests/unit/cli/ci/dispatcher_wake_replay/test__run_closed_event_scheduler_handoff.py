"""Tests for closed-event scheduler handoff handling."""

import sys
from argparse import Namespace
from typing import Any
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci import dispatcher_wake_replay as subject
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_rate_limit_handoff_renews_the_matching_wake_without_acknowledging() -> None:
    replay = Mock()
    replay.retained_wakes = {}
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:closed:123"}
    replay.scheduler_wake = ("wake", entry)
    replay.persistence_unconfirmed = False
    error = ProviderRateLimitError(reset_timestamp=900)

    with (
        patch.object(sys, "argv", ["watchdog"]),
        patch.object(subject, "_handoff_throttled", return_value=False),
        patch.object(subject, "ai_pr_loop_watchdog_command", return_value={"_rate_limit_error": error}),
    ):
        subject._run_closed_event_scheduler_handoff(
            replay,
            Namespace(mode="watchdog", repo="owner/repo", default_branch="main"),
        )

    replay._postpone_rate_limit.assert_called_once_with("wake", entry, error)
    replay.acknowledge_scheduler_handoff.assert_not_called()


def test_rate_limit_handoff_without_wake_does_not_acknowledge() -> None:
    replay = Mock()
    replay.retained_wakes = {}
    replay.scheduler_wake = None
    error = ProviderRateLimitError(reset_timestamp=900)

    with (
        patch.object(sys, "argv", ["watchdog"]),
        patch.object(subject, "_handoff_throttled", return_value=False),
        patch.object(subject, "ai_pr_loop_watchdog_command", return_value={"_rate_limit_error": error}),
    ):
        subject._run_closed_event_scheduler_handoff(
            replay,
            Namespace(mode="watchdog", repo="owner/repo", default_branch="main"),
        )

    replay._postpone_rate_limit.assert_not_called()
    replay.acknowledge_scheduler_handoff.assert_not_called()


STALLED_DISPATCH: dict[str, Any] = {
    "decision": "stalled_unaddressed_reviews",
    "throttled": False,
    "dispatched": True,
    "availability_established": True,
}


@pytest.mark.parametrize(("throttled", "acknowledged"), [(True, False), (False, True)])
def test_stalled_review_dispatch_acknowledges_only_outside_throttler_cooldown(throttled, acknowledged) -> None:
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:closed:123"}
    store = Mock()
    store.acknowledge.return_value = True
    replay = subject.DispatcherWakeReplay(Mock(), store)
    replay.scheduler_wake = ("wake", entry)

    with (
        patch.object(sys, "argv", ["watchdog"]),
        patch.object(subject, "_handoff_throttled", return_value=throttled),
        patch.object(subject, "ai_pr_loop_watchdog_command", return_value=dict(STALLED_DISPATCH)) as watchdog,
    ):
        subject._run_closed_event_scheduler_handoff(
            replay,
            Namespace(mode="watchdog", repo="owner/repo", default_branch="main"),
        )

    assert watchdog.call_count == (0 if throttled else 1)
    assert store.acknowledge.called is acknowledged


@pytest.mark.parametrize(
    "error",
    [ProviderRateLimitError(retry_after_seconds=500), RetryableError("limited", retry_after=500, is_rate_limit=True)],
)
@pytest.mark.parametrize("persisted", [True, False])
def test_throttle_lookup_rate_limit_preserves_deadline_or_fails_closed(error, persisted):
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:closed"}
    store = Mock()
    store.postpone.return_value = persisted
    replay = subject.DispatcherWakeReplay(Mock(), store)
    replay.scheduler_wake = ("wake", entry)
    with (
        patch.object(subject, "_handoff_throttled", side_effect=error),
        patch.object(subject.time, "time", return_value=100.0),
        patch.object(subject, "persist_cooldown", return_value=None),
        patch.object(subject, "ai_pr_loop_watchdog_command") as watchdog,
    ):
        if persisted:
            subject._run_closed_event_scheduler_handoff(
                replay, Namespace(mode="watchdog", repo="owner/repo", default_branch="main")
            )
        else:
            with pytest.raises(SystemExit):
                subject._run_closed_event_scheduler_handoff(
                    replay, Namespace(mode="watchdog", repo="owner/repo", default_branch="main")
                )
    watchdog.assert_not_called()
    store.acknowledge.assert_not_called()
    assert store.postpone.call_args.args[2] >= 600.0
    assert replay.persistence_unconfirmed is not persisted


def test_permission_denied_throttle_lookup_is_visible_failure(capsys):
    entry = {"pr_number": 42, "head_sha": "a" * 40, "event": "pull_request_target:closed"}
    store = Mock()
    replay = subject.DispatcherWakeReplay(Mock(), store)
    replay.scheduler_wake = ("wake", entry)
    with (
        patch.object(subject, "_handoff_throttled", side_effect=RuntimeError("HTTP 403 permission denied")),
        patch.object(subject, "ai_pr_loop_watchdog_command") as watchdog,
        pytest.raises(SystemExit),
    ):
        subject._run_closed_event_scheduler_handoff(
            replay, Namespace(mode="watchdog", repo="owner/repo", default_branch="main")
        )
    watchdog.assert_not_called()
    store.acknowledge.assert_not_called()
    assert replay.dispatch_failed
    assert "::error::" in capsys.readouterr().out


def test_throttle_lookup_failure_without_wake_propagates():
    replay = subject.DispatcherWakeReplay(Mock(), Mock())
    with (
        patch.object(subject, "_handoff_throttled", side_effect=RuntimeError("unavailable")),
        pytest.raises(RuntimeError, match="unavailable"),
    ):
        subject._run_closed_event_scheduler_handoff(
            replay, Namespace(mode="watchdog", repo="owner/repo", default_branch="main")
        )


def test_future_retained_deadline_blocks_lookup_and_watchdog():
    replay = subject.DispatcherWakeReplay(Mock(), Mock())
    replay.retained_wakes = {"wake": {"resume_at": 900.0}}
    with (
        patch.object(subject.time, "time", return_value=100.0),
        patch.object(subject, "_handoff_throttled") as throttle,
        patch.object(subject, "ai_pr_loop_watchdog_command") as watchdog,
    ):
        subject._run_closed_event_scheduler_handoff(
            replay, Namespace(mode="watchdog", repo="owner/repo", default_branch="main")
        )
    throttle.assert_not_called()
    watchdog.assert_not_called()
