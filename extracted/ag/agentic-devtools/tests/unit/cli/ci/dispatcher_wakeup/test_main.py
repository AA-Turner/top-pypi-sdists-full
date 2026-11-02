"""Tests for the durable producer CLI."""

from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import dispatcher_wakeup as subject
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_invokes_selected_mode(monkeypatch):
    runner = Mock()
    monkeypatch.setattr(subject, "DispatcherWakeup", Mock(return_value=runner))
    subject.main(["--mode", "dispatch", "--default-branch", "release"])
    runner.run.assert_called_once_with(mode="dispatch", default_branch="release")


@pytest.mark.parametrize(
    "error",
    [OSError("missing"), RuntimeError("failed"), ValueError("invalid"), ProviderRateLimitError(60), RetryableError()],
)
def test_errors_remain_visible_and_fail_the_step(monkeypatch, capsys, error):
    runner = Mock()
    runner.run.side_effect = error
    monkeypatch.setattr(subject, "DispatcherWakeup", Mock(return_value=runner))
    with pytest.raises(SystemExit) as caught:
        subject.main(["--mode", "check", "--default-branch", "main"])
    assert caught.value.code == 1
    assert f"::error::{error}" in capsys.readouterr().err


@pytest.mark.parametrize("args", [[], ["--mode", "check"], ["--mode", "invalid", "--default-branch", "main"]])
def test_requires_valid_mode_and_default_branch(args):
    with pytest.raises(SystemExit) as caught:
        subject.main(args)
    assert caught.value.code == 2
