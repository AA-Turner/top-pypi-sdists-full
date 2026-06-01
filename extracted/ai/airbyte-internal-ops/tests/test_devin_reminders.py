# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the devin_reminders module."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.devin_reminders import (
    PACIFIC_TZ,
    compute_remind_at,
    validate_delay_minutes,
)

# ---------------------------------------------------------------------------
# validate_delay_minutes
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "minutes",
    [
        pytest.param(30, id="minimum"),
        pytest.param(60, id="one_hour"),
        pytest.param(1440, id="one_day"),
        pytest.param(10080, id="seven_days_max"),
    ],
)
def test_validate_delay_minutes_valid(minutes: int) -> None:
    """Valid multiples of 30 within the 7-day limit should not raise."""
    validate_delay_minutes(minutes)


@pytest.mark.unit
@pytest.mark.parametrize(
    "minutes,match",
    [
        pytest.param(0, "must be positive", id="zero"),
        pytest.param(-30, "must be positive", id="negative"),
        pytest.param(15, "must be a multiple of 30", id="not_multiple"),
        pytest.param(45, "must be a multiple of 30", id="not_multiple_45"),
        pytest.param(10110, "must be at most", id="exceeds_max"),
    ],
)
def test_validate_delay_minutes_invalid(minutes: int, match: str) -> None:
    """Invalid values should raise ValueError with a descriptive message."""
    with pytest.raises(ValueError, match=match):
        validate_delay_minutes(minutes)


# ---------------------------------------------------------------------------
# compute_remind_at — mutual-exclusion validation
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_compute_remind_at_both_provided() -> None:
    """Providing both params raises ValueError."""
    with pytest.raises(ValueError, match="not both"):
        compute_remind_at(delay_minutes=30, remind_at_local_time="2099-01-01 09:00")


@pytest.mark.unit
def test_compute_remind_at_neither_provided() -> None:
    """Providing neither param raises ValueError."""
    with pytest.raises(ValueError, match="exactly one"):
        compute_remind_at()


# ---------------------------------------------------------------------------
# compute_remind_at — delay_minutes path
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "minutes",
    [
        pytest.param(30, id="30m"),
        pytest.param(60, id="1h"),
        pytest.param(1440, id="1d"),
    ],
)
def test_compute_remind_at_delay_minutes(minutes: int) -> None:
    """delay_minutes path returns a future UTC ISO timestamp ~minutes from now."""
    before = datetime.now(tz=timezone.utc)
    result = compute_remind_at(delay_minutes=minutes)
    after = datetime.now(tz=timezone.utc)

    parsed = datetime.fromisoformat(result)
    assert parsed.tzinfo is not None
    expected_earliest = before + timedelta(minutes=minutes)
    expected_latest = after + timedelta(minutes=minutes)
    assert expected_earliest <= parsed <= expected_latest


@pytest.mark.unit
def test_compute_remind_at_delay_minutes_invalid() -> None:
    """Invalid delay_minutes are rejected via validate_delay_minutes."""
    with pytest.raises(ValueError, match="must be a multiple of 30"):
        compute_remind_at(delay_minutes=15)


# ---------------------------------------------------------------------------
# compute_remind_at — remind_at_local_time path
# ---------------------------------------------------------------------------

_FIXED_NOW = datetime(2026, 4, 2, 20, 0, 0, tzinfo=timezone.utc)  # 1pm Pacific


@pytest.mark.unit
@pytest.mark.parametrize(
    "local_time_str,expected_utc_hour",
    [
        pytest.param("2026-04-02 14:00", 21, id="24h_format"),
        pytest.param("2026-04-02 2:00 PM", 21, id="12h_format"),
        pytest.param("2026-04-02T14:00", 21, id="iso_T_separator"),
        pytest.param("2026-04-02 17:30", 0, id="evening_pacific"),
    ],
)
def test_compute_remind_at_local_time(
    local_time_str: str, expected_utc_hour: int
) -> None:
    """Local-time strings are interpreted as Pacific and converted to UTC."""
    with patch(
        "airbyte_ops_mcp.devin_reminders.datetime",
        wraps=datetime,
    ) as mock_dt:
        mock_dt.now.return_value = _FIXED_NOW
        result = compute_remind_at(remind_at_local_time=local_time_str)

    parsed = datetime.fromisoformat(result)
    assert parsed.tzinfo is not None
    assert parsed.hour == expected_utc_hour


@pytest.mark.unit
@pytest.mark.parametrize(
    "tz_input",
    [
        pytest.param("2026-04-02T14:00:00Z", id="trailing_Z"),
        pytest.param("2026-04-02T14:00:00+00:00", id="utc_offset"),
        pytest.param("2026-04-02T14:00:00-07:00", id="pacific_offset"),
        pytest.param("2026-04-02T14:00:00+05:30", id="ist_offset"),
        pytest.param("2026-04-02T14:00:00+0530", id="ist_no_colon"),
        pytest.param("2026-04-02T14:00:00-0700", id="pacific_no_colon"),
        pytest.param("2026-04-02T14:00:00+05", id="hour_only_offset"),
        pytest.param("2026-04-02 14:00 +05:00", id="space_separated_offset"),
        pytest.param("2026-04-02 14:00 Z", id="space_separated_Z"),
    ],
)
def test_compute_remind_at_local_time_rejects_explicit_tz(tz_input: str) -> None:
    """Inputs with explicit timezone offsets are rejected."""
    with pytest.raises(ValueError, match="must not include a timezone"):
        compute_remind_at(remind_at_local_time=tz_input)


@pytest.mark.unit
def test_compute_remind_at_local_time_in_the_past() -> None:
    """A local-time string that resolves to the past raises ValueError."""
    with pytest.raises(ValueError, match="must be in the future"):
        compute_remind_at(remind_at_local_time="2020-01-01 09:00")


@pytest.mark.unit
def test_compute_remind_at_local_time_too_far() -> None:
    """A local-time string more than 7 days away raises ValueError."""
    far_future = (datetime.now(tz=PACIFIC_TZ) + timedelta(days=8)).strftime(
        "%Y-%m-%d %H:%M"
    )
    with pytest.raises(ValueError, match="at most"):
        compute_remind_at(remind_at_local_time=far_future)


@pytest.mark.unit
def test_compute_remind_at_local_time_whitespace_stripped() -> None:
    """Leading/trailing whitespace in the local-time string is tolerated."""
    with patch(
        "airbyte_ops_mcp.devin_reminders.datetime",
        wraps=datetime,
    ) as mock_dt:
        mock_dt.now.return_value = _FIXED_NOW
        result = compute_remind_at(remind_at_local_time="  2026-04-02 14:00  ")

    parsed = datetime.fromisoformat(result)
    assert parsed.hour == 21  # 2pm Pacific = 9pm UTC (PDT, UTC-7)
