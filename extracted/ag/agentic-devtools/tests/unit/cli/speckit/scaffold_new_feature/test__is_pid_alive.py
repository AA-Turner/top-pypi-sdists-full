"""Tests for ``_is_pid_alive``."""

import os
import sys
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_new_feature import _is_pid_alive


def test_returns_false_for_nonpositive_pid() -> None:
    assert _is_pid_alive(0) is False
    assert _is_pid_alive(-1) is False


def test_returns_true_for_current_process() -> None:
    assert _is_pid_alive(os.getpid()) is True


def test_returns_true_for_running_posix_process() -> None:
    with patch.object(sys, "platform", "linux"), patch("os.kill") as mock_kill:
        assert _is_pid_alive(12345) is True
        mock_kill.assert_called_once_with(12345, 0)


def test_returns_false_for_dead_pid() -> None:
    with patch.object(sys, "platform", "linux"), patch("os.kill", side_effect=ProcessLookupError):
        assert _is_pid_alive(99999) is False


def test_returns_true_when_permission_denied() -> None:
    with patch.object(sys, "platform", "linux"), patch("os.kill", side_effect=PermissionError):
        assert _is_pid_alive(1) is True
