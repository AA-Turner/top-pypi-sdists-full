"""Tests for climate-control commands."""

from datetime import date
from unittest.mock import AsyncMock, call

import pytest

from daikin_onecta import ClimateControlClient


@pytest.fixture
def client() -> AsyncMock:
    """Return the protocol client used by a bound climate-control client."""
    return AsyncMock()


@pytest.fixture
def climate_control(client: AsyncMock) -> ClimateControlClient:
    """Return commands bound to a climate-control management point."""
    return ClimateControlClient(client, "gateway-1", "climateControl")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "args", "characteristic", "value"),
    [
        ("set_power", (True,), "onOffMode", "on"),
        ("set_power", (False,), "onOffMode", "off"),
        ("set_operation_mode", ("heating",), "operationMode", "heating"),
        ("set_mode_characteristic", ("econoMode", True), "econoMode", "on"),
        ("set_mode_characteristic", ("econoMode", False), "econoMode", "off"),
    ],
)
async def test_climate_control_simple_commands(
    client: AsyncMock,
    climate_control: ClimateControlClient,
    method: str,
    args: tuple[object, ...],
    characteristic: str,
    value: str,
) -> None:
    """Use the appropriate characteristic for each simple climate command."""
    await getattr(climate_control, method)(*args)

    client.patch_characteristic.assert_awaited_once_with(
        "gateway-1",
        "climateControl",
        characteristic,
        value,
        path=None,
    )


@pytest.mark.asyncio
async def test_set_temperature(client: AsyncMock, climate_control: ClimateControlClient) -> None:
    """Set a temperature through the documented nested setpoint path."""
    await climate_control.set_temperature("heating", "roomTemperature", 21.5)

    client.patch_characteristic.assert_awaited_once_with(
        "gateway-1",
        "climateControl",
        "temperatureControl",
        21.5,
        path="/operationModes/heating/setpoints/roomTemperature",
    )


@pytest.mark.asyncio
async def test_set_fan_commands(client: AsyncMock, climate_control: ClimateControlClient) -> None:
    """Set fan speed and direction through their documented nested paths."""
    await climate_control.set_fan_mode("cooling", "quiet")
    await climate_control.set_fixed_fan_speed("cooling", 3)
    await climate_control.set_fan_direction("cooling", "vertical", "swing")
    await climate_control.set_fan_direction("cooling", "horizontal", "stop")

    assert client.patch_characteristic.await_args_list == [
        call(
            "gateway-1",
            "climateControl",
            "fanControl",
            "quiet",
            path="/operationModes/cooling/fanSpeed/currentMode",
        ),
        call(
            "gateway-1",
            "climateControl",
            "fanControl",
            3,
            path="/operationModes/cooling/fanSpeed/modes/fixed",
        ),
        call(
            "gateway-1",
            "climateControl",
            "fanControl",
            "swing",
            path="/operationModes/cooling/fanDirection/vertical/currentMode",
        ),
        call(
            "gateway-1",
            "climateControl",
            "fanControl",
            "stop",
            path="/operationModes/cooling/fanDirection/horizontal/currentMode",
        ),
    ]


@pytest.mark.asyncio
async def test_set_holiday_mode(client: AsyncMock, climate_control: ClimateControlClient) -> None:
    """Use the holiday endpoint and required dates when enabling holiday mode."""
    await climate_control.set_holiday_mode(
        True,
        start_date=date(2026, 10, 5),
        end_date=date(2026, 12, 4),
    )

    client.post_management_point.assert_awaited_once_with(
        "gateway-1",
        "climateControl",
        "holiday-mode",
        {"enabled": True, "startDate": "2026-10-05", "endDate": "2026-12-04"},
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("enabled", "start_date", "end_date"),
    [(True, None, None), (False, date(2026, 10, 5), date(2026, 12, 4))],
)
async def test_set_holiday_mode_rejects_invalid_dates(
    client: AsyncMock,
    climate_control: ClimateControlClient,
    enabled: bool,
    start_date: date | None,
    end_date: date | None,
) -> None:
    """Reject invalid holiday-mode payloads before a cloud request."""
    with pytest.raises(ValueError):
        await climate_control.set_holiday_mode(
            enabled,
            start_date=start_date,
            end_date=end_date,
        )

    client.post_management_point.assert_not_awaited()
