"""Tests for firmware commands."""

from unittest.mock import AsyncMock

import pytest

from daikin_onecta import FirmwareClient


@pytest.mark.asyncio
async def test_install_firmware() -> None:
    """Start installation of the selected offered firmware version."""
    client = AsyncMock()
    firmware = FirmwareClient(client, "gateway-1", "gateway")

    await firmware.install("firmware-1")

    client.put_management_point.assert_awaited_once_with(
        "gateway-1",
        "gateway",
        "firmware/firmware-1",
    )
