"""Firmware commands for the Daikin Onecta cloud API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import OnectaClient


class FirmwareClient:
    """Execute firmware commands for one management point."""

    def __init__(
        self,
        client: OnectaClient,
        gateway_id: str,
        management_point_id: str,
    ) -> None:
        """Initialize the firmware command client."""
        self._client = client
        self._gateway_id = gateway_id
        self._management_point_id = management_point_id

    async def install(self, firmware_id: str) -> None:
        """Start installation of an offered firmware version."""
        await self._client.put_management_point(
            self._gateway_id,
            self._management_point_id,
            f"firmware/{firmware_id}",
        )
