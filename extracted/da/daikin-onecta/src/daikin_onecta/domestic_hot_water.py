"""Domestic-hot-water commands for the Daikin Onecta cloud API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import OnectaClient


class DomesticHotWaterClient:
    """Execute commands for one domestic-hot-water management point."""

    def __init__(
        self,
        client: OnectaClient,
        gateway_id: str,
        management_point_id: str,
    ) -> None:
        """Initialize the domestic-hot-water command client."""
        self._client = client
        self._gateway_id = gateway_id
        self._management_point_id = management_point_id

    async def set_power(self, enabled: bool) -> None:
        """Turn the domestic-hot-water management point on or off."""
        await self._patch("onOffMode", "on" if enabled else "off")

    async def set_powerful_mode(self, enabled: bool) -> None:
        """Enable or disable the native powerful domestic-hot-water mode."""
        await self._patch("powerfulMode", "on" if enabled else "off")

    async def set_temperature(self, value: int | float) -> None:
        """Set the domestic-hot-water temperature target."""
        await self._patch(
            "temperatureControl",
            value,
            path="/operationModes/heating/setpoints/domesticHotWaterTemperature",
        )

    async def _patch(
        self,
        characteristic: str,
        value: int | float | str,
        *,
        path: str | None = None,
    ) -> None:
        """Patch a domestic-hot-water characteristic."""
        await self._client.patch_characteristic(
            self._gateway_id,
            self._management_point_id,
            characteristic,
            value,
            path=path,
        )
