"""Tests for the closed-event handoff throttle guard."""

from argparse import Namespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci import dispatcher_wake_replay as subject

ARGS = Namespace(mode="watchdog", repo="owner/repo", default_branch="main")


@pytest.mark.parametrize("throttled", [True, False])
def test_uses_replay_active_run_and_cooldown_guard(throttled) -> None:
    with patch.object(subject, "DispatcherThrottle") as throttle:
        throttle.return_value._lookup_last_run.return_value = {"status": "completed"}
        throttle.return_value._is_throttled.return_value = throttled
        assert subject._handoff_throttled(ARGS) is throttled

    throttle.assert_called_once_with(max_attempts=1, retry_window_seconds=0)
    throttle.return_value._lookup_last_run.assert_called_once_with("owner/repo", "main")
    throttle.return_value._is_throttled.assert_called_once_with({"status": "completed"})


def test_unknown_throttle_state_propagates_to_replay_error_handling() -> None:
    with patch.object(subject, "DispatcherThrottle") as throttle:
        throttle.return_value._lookup_last_run.side_effect = RuntimeError("unavailable")
        with pytest.raises(RuntimeError, match="unavailable"):
            subject._handoff_throttled(ARGS)
