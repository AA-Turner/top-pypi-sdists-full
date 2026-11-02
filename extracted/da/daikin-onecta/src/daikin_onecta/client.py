"""Client for the Daikin Onecta cloud API."""

import json
from collections.abc import Awaitable, Callable
from datetime import date
from typing import Any

import aiohttp
from mashumaro.exceptions import MissingField

from .air_purification import AirPurificationClient
from .climate import ClimateControlClient
from .domestic_hot_water import DomesticHotWaterClient
from .exceptions import (
    OnectaApiError,
    OnectaAuthenticationError,
    OnectaConnectionError,
    OnectaRateLimitError,
    OnectaRequestError,
    OnectaResponseError,
)
from .firmware import FirmwareClient
from .management_point import ManagementPointClient
from .models import GatewayDevice, Site
from .rate_limit import RateLimit
from .schedule import ScheduleClient

ONECTA_API_URL = "https://api.onecta.daikineurope.com"


class OnectaClient:
    """Async client for the Daikin Onecta cloud API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token_provider: Callable[[], Awaitable[str]],
        *,
        base_url: str = ONECTA_API_URL,
    ) -> None:
        """Initialize the client."""
        self._session = session
        self._token_provider = token_provider
        self._base_url = base_url.rstrip("/")
        self.rate_limit = RateLimit()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json_data: Any = None,
    ) -> Any:
        """Perform an authenticated request to the Daikin Onecta API."""
        token = await self._token_provider()
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            async with self._session.request(
                method,
                f"{self._base_url}{path}",
                headers=headers,
                json=json_data,
            ) as response:
                self.rate_limit = RateLimit.from_headers(response.headers)
                response_text = await response.text()

                if response.status in (401, 403):
                    raise OnectaAuthenticationError(response.status, method=method, path=path)

                if response.status == 429:
                    raise OnectaRateLimitError(self.rate_limit, method=method, path=path)

                if response.status >= 400:
                    raise OnectaApiError(response.status, response_text, method=method, path=path)

                if response.status == 204 or not response_text:
                    return None

                try:
                    return json.loads(response_text)
                except json.JSONDecodeError as err:
                    raise OnectaResponseError(
                        response.status,
                        "Invalid JSON response",
                        method=method,
                        path=path,
                    ) from err
        except OnectaRequestError:
            raise
        except (TimeoutError, aiohttp.ClientError) as err:
            raise OnectaConnectionError(str(err), method=method, path=path) from err

    async def get_gateway_devices(self) -> list[GatewayDevice]:
        """Return all gateway devices available to the account."""
        data = await self._request("GET", "/v1/gateway-devices")
        if not isinstance(data, list):
            raise OnectaResponseError(
                200,
                "Expected a list of gateway devices",
                method="GET",
                path="/v1/gateway-devices",
            )
        try:
            return [GatewayDevice.from_dict(device) for device in data]
        except (MissingField, TypeError, ValueError) as err:
            raise OnectaResponseError(
                200,
                "Invalid gateway device data",
                method="GET",
                path="/v1/gateway-devices",
            ) from err

    async def get_sites(self) -> list[Site]:
        """Return the account's sites and linked gateway devices."""
        data = await self._request("GET", "/v1/sites")
        if not isinstance(data, list):
            raise OnectaResponseError(
                200,
                "Expected a list of sites",
                method="GET",
                path="/v1/sites",
            )
        try:
            return [Site.from_dict(site) for site in data]
        except (MissingField, TypeError, ValueError) as err:
            raise OnectaResponseError(
                200,
                "Invalid site data",
                method="GET",
                path="/v1/sites",
            ) from err

    async def set_schedule(
        self,
        gateway_id: str,
        management_point_id: str,
        mode: str,
        schedule: str,
        *,
        enabled: bool = True,
    ) -> None:
        """Select or disable a configured schedule for a management-point mode.

        This compatibility helper delegates to :meth:`schedule`.
        New callers should use the bound schedule client.
        """
        await self.schedule(gateway_id, management_point_id).set_current(
            mode,
            schedule,
            enabled=enabled,
        )

    async def set_holiday_mode(
        self,
        gateway_id: str,
        management_point_id: str,
        enabled: bool,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> None:
        """Enable or disable holiday mode for a management point.

        This compatibility helper delegates to :meth:`climate_control`.
        New callers should use the bound climate-control client.
        """
        await self.climate_control(gateway_id, management_point_id).set_holiday_mode(
            enabled,
            start_date=start_date,
            end_date=end_date,
        )

    def climate_control(self, gateway_id: str, management_point_id: str) -> ClimateControlClient:
        """Return commands bound to one climate-control management point."""
        return ClimateControlClient(self, gateway_id, management_point_id)

    def air_purification(self, gateway_id: str, management_point_id: str) -> AirPurificationClient:
        """Return commands bound to one air-purification management point."""
        return AirPurificationClient(self, gateway_id, management_point_id)

    def management_point(self, gateway_id: str, management_point_id: str) -> ManagementPointClient:
        """Return generic commands bound to one management point."""
        return ManagementPointClient(self, gateway_id, management_point_id)

    def domestic_hot_water(self, gateway_id: str, management_point_id: str) -> DomesticHotWaterClient:
        """Return commands bound to one domestic-hot-water management point."""
        return DomesticHotWaterClient(self, gateway_id, management_point_id)

    def schedule(self, gateway_id: str, management_point_id: str) -> ScheduleClient:
        """Return schedule commands bound to one management point."""
        return ScheduleClient(self, gateway_id, management_point_id)

    async def install_firmware(
        self,
        gateway_id: str,
        management_point_id: str,
        firmware_id: str,
    ) -> None:
        """Start installation of an offered firmware version.

        This compatibility helper delegates to :meth:`firmware`.
        New callers should use the bound firmware client.
        """
        await self.firmware(gateway_id, management_point_id).install(firmware_id)

    def firmware(self, gateway_id: str, management_point_id: str) -> FirmwareClient:
        """Return firmware commands bound to one management point."""
        return FirmwareClient(self, gateway_id, management_point_id)

    async def patch_characteristic(
        self,
        gateway_id: str,
        management_point_id: str,
        characteristic: str,
        value: Any,
        *,
        path: str | None = None,
    ) -> None:
        """Set a management-point characteristic."""
        body: dict[str, Any] = {"value": value}
        if path:
            body["path"] = path
        await self._request(
            "PATCH",
            f"/v1/gateway-devices/{gateway_id}/management-points/{management_point_id}"
            f"/characteristics/{characteristic}",
            json_data=body,
        )

    async def post_management_point(
        self,
        gateway_id: str,
        management_point_id: str,
        resource: str,
        value: Any,
    ) -> Any:
        """POST data to a management-point resource."""
        return await self._request(
            "POST",
            f"/v1/gateway-devices/{gateway_id}/management-points/{management_point_id}/{resource}",
            json_data=value,
        )

    async def put_management_point(
        self,
        gateway_id: str,
        management_point_id: str,
        resource: str,
        value: Any = None,
    ) -> Any:
        """PUT data to a management-point resource."""
        return await self._request(
            "PUT",
            f"/v1/gateway-devices/{gateway_id}/management-points/{management_point_id}/{resource}",
            json_data=value,
        )
