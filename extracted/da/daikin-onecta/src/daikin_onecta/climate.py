"""Climate-control commands for the Daikin Onecta cloud API."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .client import OnectaClient


class ClimateControlClient:
    """Execute commands for one ``climateControl`` management point.

    The client is deliberately scoped to a gateway and management point. This
    keeps ONECTA characteristic names and JSON-pointer paths out of consumers
    while leaving feature discovery to the management-point model.
    """

    def __init__(
        self,
        client: OnectaClient,
        gateway_id: str,
        management_point_id: str,
    ) -> None:
        """Initialize the climate-control command client."""
        self._client = client
        self._gateway_id = gateway_id
        self._management_point_id = management_point_id

    async def set_power(self, enabled: bool) -> None:
        """Turn the climate-control management point on or off."""
        await self._patch("onOffMode", "on" if enabled else "off")

    async def set_operation_mode(self, mode: str) -> None:
        """Set the native Daikin operation mode."""
        await self._patch("operationMode", mode)

    async def set_temperature(
        self,
        operation_mode: str,
        target: str,
        value: int | float,
    ) -> None:
        """Set a temperature target for a native operation mode."""
        await self._patch(
            "temperatureControl",
            value,
            path=f"/operationModes/{operation_mode}/setpoints/{target}",
        )

    async def set_fan_mode(self, operation_mode: str, mode: str) -> None:
        """Set the fan-speed mode for a native operation mode."""
        await self._patch(
            "fanControl",
            mode,
            path=f"/operationModes/{operation_mode}/fanSpeed/currentMode",
        )

    async def set_fixed_fan_speed(self, operation_mode: str, speed: int) -> None:
        """Set the fixed fan speed for a native operation mode."""
        await self._patch(
            "fanControl",
            speed,
            path=f"/operationModes/{operation_mode}/fanSpeed/modes/fixed",
        )

    async def set_fan_direction(
        self,
        operation_mode: str,
        direction: Literal["vertical", "horizontal"],
        mode: str,
    ) -> None:
        """Set one fan-direction axis for a native operation mode."""
        await self._patch(
            "fanControl",
            mode,
            path=(f"/operationModes/{operation_mode}/fanDirection/{direction}/currentMode"),
        )

    async def set_mode_characteristic(self, characteristic: str, enabled: bool) -> None:
        """Set a named Daikin on/off mode characteristic."""
        await self._patch(characteristic, "on" if enabled else "off")

    async def set_holiday_mode(
        self,
        enabled: bool,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> None:
        """Enable or disable holiday mode.

        The ONECTA API requires both dates when enabling holiday mode and
        rejects dates when disabling it.
        """
        if enabled and (start_date is None or end_date is None):
            raise ValueError("Holiday mode requires start_date and end_date when enabled")
        if not enabled and (start_date is not None or end_date is not None):
            raise ValueError("Holiday mode dates must not be sent when disabled")

        value: dict[str, str | bool] = {"enabled": enabled}
        if enabled:
            assert start_date is not None
            assert end_date is not None
            value["startDate"] = start_date.isoformat()
            value["endDate"] = end_date.isoformat()
        await self._client.post_management_point(
            self._gateway_id,
            self._management_point_id,
            "holiday-mode",
            value,
        )

    async def _patch(
        self,
        characteristic: str,
        value: int | float | str,
        *,
        path: str | None = None,
    ) -> None:
        """Patch a climate-control characteristic."""
        await self._client.patch_characteristic(
            self._gateway_id,
            self._management_point_id,
            characteristic,
            value,
            path=path,
        )
