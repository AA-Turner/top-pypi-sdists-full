"""Tests for the Daikin Onecta client."""

import json
from datetime import date
from pathlib import Path

import aiohttp
import pytest
from aioresponses import aioresponses
from yarl import URL

from daikin_onecta import (
    OnectaApiError,
    OnectaAuthenticationError,
    OnectaClient,
    OnectaConnectionError,
    OnectaRateLimitError,
    OnectaResponseError,
)

BASE_URL = "https://api.onecta.daikineurope.com"
FIXTURES = Path(__file__).parent / "fixtures"


async def token_provider() -> str:
    """Return a test access token."""
    return "token"


@pytest.mark.asyncio
async def test_get_gateway_devices() -> None:
    """Return gateway devices from the API."""
    payload = [
        {
            "id": "gateway-1",
            "deviceModel": "test",
            "isCloudConnectionUp": {"value": True, "settable": False},
            "managementPoints": [],
        }
    ]

    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(
                f"{BASE_URL}/v1/gateway-devices",
                payload=payload,
                headers={"X-RateLimit-Remaining-day": "123"},
            )
            client = OnectaClient(session, token_provider)

            devices = await client.get_gateway_devices()

            assert len(devices) == 1
            assert devices[0].id == "gateway-1"
            assert devices[0].device_model == "test"
            assert devices[0].available is True
            assert client.rate_limit.day_remaining == 123


@pytest.mark.asyncio
async def test_get_gateway_devices_without_management_points() -> None:
    """Allow a gateway response where Daikin omits management points."""
    payload = json.loads((FIXTURES / "issue_841_gateway_devices.json").read_text())

    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/gateway-devices", payload=payload)
            client = OnectaClient(session, token_provider)

            devices = await client.get_gateway_devices()

    assert len(devices) == 1
    assert devices[0].id == "test-altherma-gateway"
    assert devices[0].device_type == "heating"
    assert devices[0].management_points == []


@pytest.mark.asyncio
async def test_get_sites() -> None:
    """Return the complete documented site data."""
    payload = [
        {
            "id": "site-1",
            "name": "Home",
            "role": "admin",
            "location": {
                "countryCode": "NL",
                "placeID": "NL/GEO/p0/1",
                "latitude": 52.0,
                "longitude": 5.0,
                "level": "municipality",
            },
            "users": [{"id": "user-1", "role": "admin"}],
            "gatewayDevices": ["gateway-1", "gateway-2"],
        }
    ]

    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/sites", payload=payload)
            client = OnectaClient(session, token_provider)

            sites = await client.get_sites()

    site = sites[0]
    assert site.id == "site-1"
    assert site.name == "Home"
    assert site.role == "admin"
    assert site.location is not None
    assert site.location.country_code == "NL"
    assert site.location.place_id == "NL/GEO/p0/1"
    assert site.location.latitude == 52.0
    assert site.location.longitude == 5.0
    assert site.location.level == "municipality"
    assert [(user.id, user.role) for user in site.users or []] == [("user-1", "admin")]
    assert site.gateway_device_ids == ["gateway-1", "gateway-2"]
    assert site.has_gateway_device("gateway-1") is True
    assert site.has_gateway_device("gateway-3") is False


@pytest.mark.asyncio
async def test_get_sites_preserves_unknown_gateway_membership() -> None:
    """Do not treat an omitted device list as an empty one."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/sites", payload=[{"id": "site-1"}])
            client = OnectaClient(session, token_provider)

            sites = await client.get_sites()

    assert sites[0].gateway_device_ids is None
    assert sites[0].has_gateway_device("gateway-1") is None


@pytest.mark.asyncio
@pytest.mark.parametrize("payload", [None, {"id": "site-1"}, [{"id": "site-1", "gatewayDevices": "gateway-1"}]])
async def test_get_sites_rejects_invalid_responses(payload: object) -> None:
    """Reject malformed site responses."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/sites", payload=payload)
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaResponseError) as exc_info:
                await client.get_sites()

    assert exc_info.value.path == "/v1/sites"


@pytest.mark.asyncio
async def test_rate_limit_error() -> None:
    """Expose Daikin retry-after information on HTTP 429."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(
                f"{BASE_URL}/v1/gateway-devices",
                status=429,
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit-minute": "120",
                    "X-RateLimit-Remaining-day": "456",
                    "RateLimit-Reset": "1200",
                },
            )
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaRateLimitError) as exc_info:
                await client.get_gateway_devices()

            error = exc_info.value
            assert error.method == "GET"
            assert error.path == "/v1/gateway-devices"
            assert error.retry_after == 60
            assert error.rate_limit.minute_limit == 120
            assert error.rate_limit.day_remaining == 456
            assert error.rate_limit.reset == 1200


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 403])
async def test_authentication_error(status: int) -> None:
    """Translate authentication failures to a dedicated exception."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/gateway-devices", status=status)
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaAuthenticationError) as exc_info:
                await client.get_gateway_devices()

            assert exc_info.value.status == status
            assert exc_info.value.method == "GET"
            assert exc_info.value.path == "/v1/gateway-devices"


@pytest.mark.asyncio
async def test_unexpected_api_error() -> None:
    """Raise an API error instead of returning an empty device list."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/gateway-devices", status=500, body="server error")
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaApiError) as exc_info:
                await client.get_gateway_devices()

            assert exc_info.value.status == 500
            assert exc_info.value.method == "GET"
            assert exc_info.value.path == "/v1/gateway-devices"


@pytest.mark.asyncio
async def test_set_schedule() -> None:
    """Select an existing schedule through the schedule endpoint."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            url = f"{BASE_URL}/v1/gateway-devices/gateway-1/management-points/climateControl/schedule/heating/current"
            mocked.put(url, status=204)
            client = OnectaClient(session, token_provider)

            await client.set_schedule("gateway-1", "climateControl", "heating", "scheduleHeatingRT2")

            request = mocked.requests[("PUT", URL(url))][0]
            assert request.kwargs["json"] == {
                "scheduleId": "scheduleHeatingRT2",
                "enabled": True,
            }


@pytest.mark.asyncio
async def test_invalid_json_response() -> None:
    """Translate a successful non-JSON response to a response error."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/gateway-devices", status=200, body="not json")
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaResponseError, match="Invalid JSON response") as exc_info:
                await client.get_gateway_devices()

            assert exc_info.value.status == 200
            assert exc_info.value.method == "GET"
            assert exc_info.value.path == "/v1/gateway-devices"


@pytest.mark.asyncio
@pytest.mark.parametrize("payload", [None, {"id": "gateway-1"}])
async def test_gateway_devices_requires_list(payload: object) -> None:
    """Reject a gateway-device response that is not a list."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/gateway-devices", payload=payload)
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaApiError, match="Expected a list of gateway devices"):
                await client.get_gateway_devices()


@pytest.mark.asyncio
async def test_invalid_gateway_device() -> None:
    """Translate invalid gateway-device data to an API error."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/gateway-devices", payload=[{"id": "gateway-1"}])
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaApiError, match="Invalid gateway device data"):
                await client.get_gateway_devices()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error",
    [aiohttp.ClientConnectionError("offline"), TimeoutError("timed out")],
)
async def test_connection_error(error: Exception) -> None:
    """Translate connection failures to a dedicated exception."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get(f"{BASE_URL}/v1/gateway-devices", exception=error)
            client = OnectaClient(session, token_provider)

            with pytest.raises(OnectaConnectionError, match=str(error)) as exc_info:
                await client.get_gateway_devices()

            assert exc_info.value.method == "GET"
            assert exc_info.value.path == "/v1/gateway-devices"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (None, {"value": "heating"}),
        ("/operationModes/heating", {"value": 21.5, "path": "/operationModes/heating"}),
    ],
)
async def test_patch_characteristic(path: str | None, expected: dict[str, object]) -> None:
    """Patch a characteristic with an optional nested path."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            url = (
                f"{BASE_URL}/v1/gateway-devices/gateway-1/management-points/climateControl"
                "/characteristics/operationMode"
            )
            mocked.patch(url, status=204)
            client = OnectaClient(session, token_provider)

            value = "heating" if path is None else 21.5
            await client.patch_characteristic("gateway-1", "climateControl", "operationMode", value, path=path)

            request = mocked.requests[("PATCH", URL(url))][0]
            assert request.kwargs["json"] == expected


@pytest.mark.asyncio
async def test_post_management_point() -> None:
    """Return JSON data from a management-point POST."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            url = f"{BASE_URL}/v1/gateway-devices/gateway-1/management-points/climateControl/refresh"
            mocked.post(url, payload={"status": "accepted"})
            client = OnectaClient(session, token_provider)

            result = await client.post_management_point("gateway-1", "climateControl", "refresh", {"force": True})

            assert result == {"status": "accepted"}
            request = mocked.requests[("POST", URL(url))][0]
            assert request.kwargs["json"] == {"force": True}


@pytest.mark.asyncio
async def test_put_management_point_custom_base_url() -> None:
    """Normalize a custom base URL and return PUT response data."""
    base_url = "https://example.test/"
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            url = "https://example.test/v1/gateway-devices/gateway-1/management-points/climateControl/resource"
            mocked.put(url, payload={"updated": True})
            client = OnectaClient(session, token_provider, base_url=base_url)

            result = await client.put_management_point("gateway-1", "climateControl", "resource")

            assert result == {"updated": True}
            request = mocked.requests[("PUT", URL(url))][0]
            assert request.kwargs["json"] is None


@pytest.mark.asyncio
async def test_disable_schedule() -> None:
    """Disable a configured schedule."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            url = f"{BASE_URL}/v1/gateway-devices/gateway-1/management-points/climateControl/schedule/heating/current"
            mocked.put(url, status=204)
            client = OnectaClient(session, token_provider)

            await client.set_schedule(
                "gateway-1",
                "climateControl",
                "heating",
                "scheduleHeatingRT2",
                enabled=False,
            )

            request = mocked.requests[("PUT", URL(url))][0]
            assert request.kwargs["json"] == {
                "scheduleId": "scheduleHeatingRT2",
                "enabled": False,
            }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("enabled", "start_date", "end_date", "expected"),
    [
        (
            True,
            date(2026, 10, 5),
            date(2026, 12, 4),
            {"enabled": True, "startDate": "2026-10-05", "endDate": "2026-12-04"},
        ),
        (False, None, None, {"enabled": False}),
    ],
)
async def test_set_holiday_mode(
    enabled: bool,
    start_date: date | None,
    end_date: date | None,
    expected: dict[str, str | bool],
) -> None:
    """Set holiday mode through its typed API endpoint."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            url = f"{BASE_URL}/v1/gateway-devices/gateway-1/management-points/climateControl/holiday-mode"
            mocked.post(url, status=204)
            client = OnectaClient(session, token_provider)

            await client.set_holiday_mode(
                "gateway-1",
                "climateControl",
                enabled,
                start_date=start_date,
                end_date=end_date,
            )

            request = mocked.requests[("POST", URL(url))][0]
            assert request.kwargs["json"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("enabled", "start_date", "end_date"),
    [(True, None, None), (False, date(2026, 10, 5), date(2026, 12, 4))],
)
async def test_set_holiday_mode_rejects_invalid_dates(
    enabled: bool,
    start_date: date | None,
    end_date: date | None,
) -> None:
    """Reject invalid holiday-mode payloads before making a cloud request."""
    async with aiohttp.ClientSession() as session:
        client = OnectaClient(session, token_provider)

        with pytest.raises(ValueError):
            await client.set_holiday_mode(
                "gateway-1",
                "climateControl",
                enabled,
                start_date=start_date,
                end_date=end_date,
            )


@pytest.mark.asyncio
async def test_install_firmware() -> None:
    """Start a firmware installation through its typed API endpoint."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            url = f"{BASE_URL}/v1/gateway-devices/gateway-1/management-points/gateway/firmware/firmware-1"
            mocked.put(url, status=204)
            client = OnectaClient(session, token_provider)

            await client.install_firmware("gateway-1", "gateway", "firmware-1")

            request = mocked.requests[("PUT", URL(url))][0]
            assert request.kwargs["json"] is None
