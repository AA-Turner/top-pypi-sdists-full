"""Tests for the supervision_control_command symbol."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.supervision_control_command import supervision_control_command


@pytest.mark.parametrize("failure", [RuntimeError("provider failed"), ValueError("invalid input")])
def test_supervision_control_command_reports_domain_failures(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: Exception,
) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.supervision_control_command.main",
        lambda: (_ for _ in ()).throw(failure),
    )

    with pytest.raises(SystemExit) as exc_info:
        supervision_control_command()

    assert exc_info.value.code == 1
    assert capsys.readouterr().err == f"Error: {failure}\n"


def test_supervision_control_command_preserves_success_exit_code(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command.main", lambda: 0)

    with pytest.raises(SystemExit) as exc_info:
        supervision_control_command()

    assert exc_info.value.code == 0
