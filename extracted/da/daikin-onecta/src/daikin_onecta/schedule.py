"""Schedule commands for the Daikin Onecta cloud API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import OnectaClient


class ScheduleClient:
    """Execute schedule commands for one management point."""

    def __init__(
        self,
        client: OnectaClient,
        gateway_id: str,
        management_point_id: str,
    ) -> None:
        """Initialize the schedule command client."""
        self._client = client
        self._gateway_id = gateway_id
        self._management_point_id = management_point_id

    async def set_current(
        self,
        mode: str,
        schedule_id: str,
        *,
        enabled: bool = True,
    ) -> None:
        """Select or disable a configured schedule for an operation mode."""
        await self._client.put_management_point(
            self._gateway_id,
            self._management_point_id,
            f"schedule/{mode}/current",
            {"scheduleId": schedule_id, "enabled": enabled},
        )
