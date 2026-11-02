"""Confirmed process-group cleanup, including already completed leaders."""

import os
import signal
from unittest.mock import Mock, call, patch

import pytest

from agentic_devtools.cli.checks import pre_push_budget

pytestmark = pytest.mark.skipif(os.name != "posix", reason="Requires POSIX process-group probing")


def test_absent_group_is_not_signalled():
    process = Mock(pid=12345)
    with patch.object(pre_push_budget.os, "killpg", side_effect=ProcessLookupError) as killpg:
        assert pre_push_budget._stop_group(process)
    process.poll.assert_called_once_with()
    killpg.assert_called_once_with(process.pid, 0)


def test_group_disappears_between_probe_and_signal():
    process = Mock(pid=12345)
    with patch.object(
        pre_push_budget.os, "killpg", side_effect=[None, ProcessLookupError, ProcessLookupError]
    ) as killpg:
        assert pre_push_budget._stop_group(process)
    assert killpg.call_args_list == [call(process.pid, 0), call(process.pid, signal.SIGTERM), call(process.pid, 0)]


def test_completed_leader_status_is_recorded_before_descendant_cleanup():
    process = Mock(pid=12345)
    process.poll.return_value = 10
    status = []
    with patch.object(pre_push_budget.os, "killpg", side_effect=ProcessLookupError):
        assert pre_push_budget._stop_group(process, status)
    assert status == [10]
