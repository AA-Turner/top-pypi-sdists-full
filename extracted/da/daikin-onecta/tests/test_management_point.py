"""Tests for generic management-point commands."""

from unittest.mock import AsyncMock

import pytest

from daikin_onecta import AirPurificationClient, ManagementPointClient, OnectaClient


@pytest.mark.asyncio
async def test_management_point_commands() -> None:
    """Bind generic characteristic and resource commands to a management point."""
    client = AsyncMock()
    management_point = ManagementPointClient(client, "gateway-1", "zone-1")

    await management_point.set_characteristic("onOffMode", "on")
    await management_point.set_characteristic("fanControl", "auto", path="/currentMode")
    await management_point.post("resource", {"enabled": True})
    await management_point.put("resource")
    await management_point.put("resource", {"enabled": False})

    assert client.patch_characteristic.await_args_list[0].args == ("gateway-1", "zone-1", "onOffMode", "on")
    assert client.patch_characteristic.await_args_list[0].kwargs == {"path": None}
    assert client.patch_characteristic.await_args_list[1].args == ("gateway-1", "zone-1", "fanControl", "auto")
    assert client.patch_characteristic.await_args_list[1].kwargs == {"path": "/currentMode"}
    client.post_management_point.assert_awaited_once_with("gateway-1", "zone-1", "resource", {"enabled": True})
    assert client.put_management_point.await_args_list[0].args == ("gateway-1", "zone-1", "resource", None)
    assert client.put_management_point.await_args_list[1].args == (
        "gateway-1",
        "zone-1",
        "resource",
        {"enabled": False},
    )


def test_management_point_client_factory() -> None:
    """Create generic commands through the main client."""
    client = OnectaClient(AsyncMock(), AsyncMock())

    assert isinstance(client.management_point("gateway-1", "zone-1"), ManagementPointClient)
    assert isinstance(client.air_purification("gateway-1", "zone-1"), AirPurificationClient)
