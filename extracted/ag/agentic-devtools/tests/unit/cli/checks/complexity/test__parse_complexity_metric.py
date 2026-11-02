"""Tests for parsing the measured count from Ruff complexity diagnostics."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.complexity import _parse_complexity_metric


@pytest.mark.parametrize(
    ("rule", "message", "expected"),
    [
        ("C901", "`complicated` is too complex (15 > 10)", 15),
        ("PLR0912", "Too many branches (20 > 12)", 20),
        ("PLR0915", "Too many statements (60 > 50)", 60),
    ],
)
def test_parses_metric_for_each_complexity_rule(rule: str, message: str, expected: int) -> None:
    assert _parse_complexity_metric(rule, message) == expected


def test_rejects_unknown_complexity_rules() -> None:
    with pytest.raises(ValueError, match="unsupported complexity rule"):
        _parse_complexity_metric("C999", "`complicated` is too complex (15 > 10)")


@pytest.mark.parametrize(
    ("message", "expected_error"),
    [
        ("not a Ruff diagnostic", "unrecognized C901 complexity metric message"),
        ("`complicated` is too complex (10 > 10)", "default C901 threshold"),
        ("`complicated` is too complex (11 > 9)", "default C901 threshold"),
    ],
)
def test_rejects_invalid_complexity_metrics(message: str, expected_error: str) -> None:
    with pytest.raises(ValueError, match=expected_error):
        _parse_complexity_metric("C901", message)
