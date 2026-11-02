"""Tests for domestic-hot-water commands."""

from unittest.mock import AsyncMock, call

import pytest

from daikin_onecta import DomesticHotWaterClient, OnectaClient


async def token_provider() -> str:
    """Return a test access token."""
    return "token"


@pytest.mark.asyncio
async def test_domestic_hot_water_factory() -> None:
    """Bind domestic-hot-water commands through the main API client."""
    client = OnectaClient(AsyncMock(), token_provider)

    hot_water = client.domestic_hot_water("gateway-1", "domesticHotWater")

    assert isinstance(hot_water, DomesticHotWaterClient)


@pytest.mark.asyncio
async def test_domestic_hot_water_commands() -> None:
    """Use the expected characteristic paths for domestic-hot-water commands."""
    client = AsyncMock()
    hot_water = DomesticHotWaterClient(client, "gateway-1", "domesticHotWater")

    await hot_water.set_power(True)
    await hot_water.set_powerful_mode(False)
    await hot_water.set_temperature(55.5)

    assert client.patch_characteristic.await_args_list == [
        call("gateway-1", "domesticHotWater", "onOffMode", "on", path=None),
        call("gateway-1", "domesticHotWater", "powerfulMode", "off", path=None),
        call(
            "gateway-1",
            "domesticHotWater",
            "temperatureControl",
            55.5,
            path="/operationModes/heating/setpoints/domesticHotWaterTemperature",
        ),
    ]
