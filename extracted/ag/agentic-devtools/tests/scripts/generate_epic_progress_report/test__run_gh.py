"""Tests for _run_gh in generate_epic_progress_report."""

from __future__ import annotations

import re
import subprocess
from unittest.mock import patch

import pytest

from tests.scripts.generate_epic_progress_report import report


def test_error_message_uses_stderr_when_present():
    """Uses stderr as the error detail when it is non-empty."""
    exc = subprocess.CalledProcessError(1, ["gh"], output="", stderr="auth error")
    with patch("subprocess.run", side_effect=exc):
        with pytest.raises(RuntimeError, match="auth error"):
            report._run_gh(["whoami"])


def test_error_message_falls_back_to_stdout_when_stderr_blank():
    """Falls back to stdout when stderr is blank so the error is not empty."""
    exc = subprocess.CalledProcessError(1, ["gh"], output='{"errors":[]}', stderr="")
    with patch("subprocess.run", side_effect=exc):
        with pytest.raises(RuntimeError, match=re.escape('{"errors":[]}')):
            report._run_gh(["whoami"])


def test_error_message_includes_return_code_when_both_streams_blank():
    """Falls back to exit code when both stdout and stderr are blank."""
    exc = subprocess.CalledProcessError(2, ["gh"], output="", stderr="")
    with patch("subprocess.run", side_effect=exc):
        with pytest.raises(RuntimeError, match="exit code 2"):
            report._run_gh(["whoami"])
