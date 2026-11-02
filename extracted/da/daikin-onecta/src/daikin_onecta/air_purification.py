"""Air-purification commands for the Daikin Onecta cloud API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import OnectaClient


class AirPurificationClient:
    """Execute commands for one air-purification management point."""

    def __init__(self, client: OnectaClient, gateway_id: str, management_point_id: str) -> None:
        """Initialize commands bound to one management point."""
        self._client = client
        self._gateway_id = gateway_id
        self._management_point_id = management_point_id

    async def set_power(self, enabled: bool) -> None:
        """Turn the air-purification management point on or off."""
        await self._patch("onOffMode", "on" if enabled else "off")

    async def set_mode(self, mode: str) -> None:
        """Set the native Daikin air-purification mode."""
        await self._patch("airPurificationMode", mode)

    async def set_fixed_fan_speed(self, mode: str, speed: int) -> None:
        """Set the fixed fan speed for a native air-purification mode."""
        await self._patch("fanControl", speed, path=f"/airPurificationModes/{mode}/fanSpeed/modes/fixed")

    async def _patch(self, characteristic: str, value: int | str, *, path: str | None = None) -> None:
        """Patch an air-purification characteristic."""
        await self._client.patch_characteristic(
            self._gateway_id,
            self._management_point_id,
            characteristic,
            value,
            path=path,
        )
