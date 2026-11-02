"""Tests for the shared check result type."""

from agentic_devtools.cli.checks.check_result import _CheckResult


def test_stores_check_outcome_and_defaults_duration() -> None:
    result = _CheckResult("File length", True, "OK")

    assert result.label == "File length"
    assert result.passed is True
    assert result.output == "OK"
    assert result.duration == 0.0
