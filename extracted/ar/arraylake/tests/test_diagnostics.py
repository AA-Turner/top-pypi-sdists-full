import asyncio
from unittest.mock import patch

import httpx
import pytest

from arraylake.api_utils import ArraylakeHttpClient
from arraylake.config import config
from arraylake.diagnostics import (
    get_diagnostics,
    get_system_info,
    get_versions,
    print_diagnostics,
)


def test_get_system_info():
    info = get_system_info()
    expected_keys = ["python", "machine"]
    assert all([k in info for k in expected_keys])


def test_get_versions():
    info = get_versions()
    expected_keys = ["arraylake", "zarr", "httpx"]
    assert all([k in info for k in expected_keys])


def test_get_diagnostics():
    diagnostics = get_diagnostics().model_dump()
    assert diagnostics
    expected_keys = ["versions", "system"]
    assert all([k in diagnostics for k in expected_keys])


def test_print_diagnostics():
    print_diagnostics()


@pytest.mark.asyncio
async def test_diagnostics_post_to_api(respx_mock, test_api_token) -> None:
    with config.set({"user.diagnostics": True}):
        api_url = "https://foo.bar/"
        response_json = test_api_token.model_dump()
        response_json["id"] = str(response_json["id"])
        user_route = respx_mock.request("GET", api_url + "user").mock(side_effect=[httpx.Response(httpx.codes.OK, json=response_json)])
        diagnostics_route = respx_mock.request("POST", api_url + "user/diagnostics", content__contains="versions").mock(
            side_effect=[httpx.Response(200)]
        )

        client = ArraylakeHttpClient(api_url, token="token")
        user = await client.get_user()
        await asyncio.sleep(1)
        assert user_route.call_count == 1
        assert diagnostics_route.call_count == 1
        assert user == test_api_token


@pytest.mark.asyncio
async def test_diagnostics_config_false(respx_mock, test_api_token) -> None:
    api_url = "https://foo.bar/"
    response_json = test_api_token.model_dump()
    response_json["id"] = str(response_json["id"])

    user_route = respx_mock.request("GET", api_url + "user").mock(side_effect=[httpx.Response(httpx.codes.OK, json=response_json)])
    diagnostics_route = respx_mock.request("POST", api_url + "user/diagnostics").mock(side_effect=[httpx.Response(200)])

    with config.set({"user.diagnostics": False}):
        with patch("arraylake.diagnostics.get_diagnostics") as mock_method:
            client = ArraylakeHttpClient(api_url, token="token")
            user = await client.get_user()
            assert user_route.call_count == 1
            assert diagnostics_route.call_count == 0  # important - user has opted out of sending diagnostics
            assert user == test_api_token
            mock_method.assert_not_called()  # check that we didn't even collect the diagnostics


@pytest.mark.asyncio
async def test_failed_diagnostic_post_does_not_raise(respx_mock, test_api_token) -> None:
    with config.set({"user.diagnostics": True}):
        api_url = "https://foo.bar/"
        response_json = test_api_token.model_dump()
        response_json["id"] = str(response_json["id"])
        user_route = respx_mock.request("GET", api_url + "user").mock(side_effect=[httpx.Response(httpx.codes.OK, json=response_json)])
        diagnostics_route = respx_mock.request("POST", api_url + "user/diagnostics").mock(side_effect=[httpx.Response(400)])

        client = ArraylakeHttpClient(api_url, token="token")
        user = await client.get_user()
        await asyncio.sleep(1)
        assert user_route.call_count == 1
        assert diagnostics_route.call_count == 1
        assert user == test_api_token
