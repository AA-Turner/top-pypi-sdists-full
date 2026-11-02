"""Retained-wake errors preserve failure across all snapshots."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.dispatcher_wake_replay import _handle_retained_wake_error


def test_earlier_unconfirmed_deadline_is_not_hidden_by_later_success():
    runner = Mock(persistence_unconfirmed=False, dispatch_failed=False)
    entries = {"first": {"pr_number": 1}, "second": {"pr_number": 2}}
    error = RuntimeError("provider lookup failed")

    def handle(key, entry, exc):
        runner.persistence_unconfirmed = key == "first"

    runner._handle_replay_error.side_effect = handle
    with pytest.raises(SystemExit):
        _handle_retained_wake_error(runner, entries, error)
    assert runner._handle_replay_error.call_count == 2
