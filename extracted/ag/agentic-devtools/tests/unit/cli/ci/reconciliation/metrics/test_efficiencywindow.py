"""Tests for EfficiencyWindow."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.metrics import EfficiencyWindow


def test_rejects_naive_start_at() -> None:
    with pytest.raises(ValueError, match="timezone"):
        EfficiencyWindow(
            window_id="w1",
            start_at=datetime(2024, 1, 1),
            end_at=datetime(2024, 1, 2, tzinfo=UTC),
        )


def test_rejects_naive_end_at() -> None:
    with pytest.raises(ValueError, match="timezone"):
        EfficiencyWindow(
            window_id="w1",
            start_at=datetime(2024, 1, 1, tzinfo=UTC),
            end_at=datetime(2024, 1, 2),
        )


def test_accepts_timezone_aware_bounds() -> None:
    window = EfficiencyWindow(
        window_id="w1",
        start_at=datetime(2024, 1, 1, tzinfo=UTC),
        end_at=datetime(2024, 1, 2, tzinfo=UTC),
    )
    assert window.end_at - window.start_at == timedelta(hours=24)
