"""Generic management-point commands for the Daikin Onecta cloud API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import OnectaClient


class ManagementPointClient:
    """Execute generic commands for one management point."""

    def __init__(
        self,
        client: OnectaClient,
        gateway_id: str,
        management_point_id: str,
    ) -> None:
        """Initialize commands bound to a gateway and management point."""
        self._client = client
        self._gateway_id = gateway_id
        self._management_point_id = management_point_id

    async def set_characteristic(
        self,
        name: str,
        value: Any,
        *,
        path: str | None = None,
    ) -> None:
        """Set a characteristic, optionally at a nested JSON-pointer path."""
        await self._client.patch_characteristic(
            self._gateway_id,
            self._management_point_id,
            name,
            value,
            path=path,
        )

    async def post(self, resource: str, value: Any) -> None:
        """POST data to a management-point resource."""
        await self._client.post_management_point(
            self._gateway_id,
            self._management_point_id,
            resource,
            value,
        )

    async def put(self, resource: str, value: Any = None) -> None:
        """PUT optional data to a management-point resource."""
        await self._client.put_management_point(
            self._gateway_id,
            self._management_point_id,
            resource,
            value,
        )
