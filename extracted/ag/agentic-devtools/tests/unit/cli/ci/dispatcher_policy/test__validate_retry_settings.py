"""Tests for configurable throttle lookup retry bounds."""

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import _validate_retry_settings


@pytest.mark.parametrize(
    ("max_attempts", "retry_window_seconds"),
    [
        (True, 0),
        (1.5, 0),
        ("1", 0),
        (0, 0),
        (-1, 0),
        (1, True),
        (1, "0"),
        (1, None),
        (1, -1),
        (1, float("inf")),
        (1, float("nan")),
        (1, 10**1000),
    ],
)
def test_rejects_invalid_retry_settings(max_attempts, retry_window_seconds):
    with pytest.raises(ValueError):
        _validate_retry_settings(max_attempts, retry_window_seconds)


@pytest.mark.parametrize(("max_attempts", "retry_window_seconds"), [(1, 0), (3, 21000), (2, 1.5)])
def test_accepts_single_attempt_and_bounded_retry_settings(max_attempts, retry_window_seconds):
    _validate_retry_settings(max_attempts, retry_window_seconds)
