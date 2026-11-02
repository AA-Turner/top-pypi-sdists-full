"""Tests for schedule commands."""

from unittest.mock import AsyncMock

import pytest

from daikin_onecta import ScheduleClient


@pytest.mark.asyncio
async def test_set_current_schedule() -> None:
    """Select a configured schedule for an operation mode."""
    client = AsyncMock()
    schedule = ScheduleClient(client, "gateway-1", "climateControl")

    await schedule.set_current("heating", "scheduleHeatingRT2", enabled=False)

    client.put_management_point.assert_awaited_once_with(
        "gateway-1",
        "climateControl",
        "schedule/heating/current",
        {"scheduleId": "scheduleHeatingRT2", "enabled": False},
    )
