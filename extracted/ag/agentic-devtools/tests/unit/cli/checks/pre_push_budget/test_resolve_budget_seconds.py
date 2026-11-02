"""Budget override parsing."""

import pytest

from agentic_devtools.cli.checks.pre_push_budget import DEFAULT_BUDGET_SECONDS, resolve_budget_seconds


def test_missing_override(capsys):
    assert DEFAULT_BUDGET_SECONDS == 600
    assert resolve_budget_seconds({}) == 600
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize("value", ["1", "600", "1234", " 12 "])
def test_positive_override(value, capsys):
    assert resolve_budget_seconds({"AGDT_PRE_PUSH_BUDGET_SECONDS": value}) == int(value)
    assert capsys.readouterr().err == ""


@pytest.mark.parametrize("value", ["", "invalid", "1.5", "0", "-1"])
def test_invalid_override_warns_once(value, capsys):
    assert resolve_budget_seconds({"AGDT_PRE_PUSH_BUDGET_SECONDS": value}) == 600
    warning = capsys.readouterr().err
    assert len(warning.splitlines()) == 1
    assert "AGDT_PRE_PUSH_BUDGET_SECONDS" in warning
    assert "600" in warning
