"""Tests for air-purification commands."""

from unittest.mock import AsyncMock, call

import pytest

from daikin_onecta import AirPurificationClient


@pytest.mark.asyncio
async def test_air_purification_commands() -> None:
    """Use Daikin's documented characteristics and JSON-pointer paths."""
    client = AsyncMock()
    purification = AirPurificationClient(client, "gateway-1", "climateControl")

    await purification.set_power(True)
    await purification.set_mode("manualFan")
    await purification.set_fixed_fan_speed("manualFan", 3)

    assert client.patch_characteristic.await_args_list == [
        call("gateway-1", "climateControl", "onOffMode", "on", path=None),
        call("gateway-1", "climateControl", "airPurificationMode", "manualFan", path=None),
        call(
            "gateway-1",
            "climateControl",
            "fanControl",
            3,
            path="/airPurificationModes/manualFan/fanSpeed/modes/fixed",
        ),
    ]
