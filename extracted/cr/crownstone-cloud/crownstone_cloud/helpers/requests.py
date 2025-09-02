"""Handler for requests to the Crownstone cloud"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from aiohttp import ClientSession, ContentTypeError

from crownstone_cloud.const import DEFAULT_CLOUD_ADDR, CLOUD_LOGIN_SUFFIX
from crownstone_cloud.exceptions import (
    AuthError,
    CrownstoneAuthenticationError,
    CrownstoneConnectionError,
    CrownstoneUnknownError,
)
from crownstone_cloud.helpers.aiohttp_client import create_clientsession
from crownstone_cloud.helpers.conversion import quote_json

if TYPE_CHECKING:
    from crownstone_cloud.cloud import CrownstoneCloud

_LOGGER = logging.getLogger(__name__)


class RequestHandler:
    """Handles requests to the Crownstone cloud."""

    def __init__(
        self, cloud: CrownstoneCloud, clientsession: ClientSession | None = None
    ) -> None:
        self.cloud = cloud
        self.client_session = clientsession or create_clientsession()

    async def request_login(self, login_data: dict[str, Any]) -> Any:
        """Request a login to the Crownstone Cloud API."""
        response = await self.request("post", f"{DEFAULT_CLOUD_ADDR}{CLOUD_LOGIN_SUFFIX}", login_data)

        return response

    async def post(
        self,
        model: str,
        endpoint: str,
        model_id: str | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """
        Post request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :param json: Dictionary with the data that should be posted.
        :return: Dictionary with the response from the cloud.
        """
        if model_id:
            url = f"{DEFAULT_CLOUD_ADDR}/{model}/{model_id}/{endpoint}?access_token={self.cloud.access_token}"
        else:
            url = f"{DEFAULT_CLOUD_ADDR}/{model}{endpoint}?access_token={self.cloud.access_token}"

        return await self.request("post", url, json)

    async def get(
        self,
        model: str,
        endpoint: str,
        data_filter: dict[str, Any] | None = None,
        model_id: str | None = None,
    ) -> Any:
        """
        Get request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, preUnionentPeople.
        :param filter: filter output or add extra data to output.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :return: Dictionary with the response from the cloud.
        """
        if data_filter and model_id:
            url = (
                f"{DEFAULT_CLOUD_ADDR}/{model}/{model_id}/{endpoint}?filter={quote_json(data_filter)}&access_token="
                f"{self.cloud.access_token}"
            )
        elif model_id and not data_filter:
            url = f"{DEFAULT_CLOUD_ADDR}/{model}/{model_id}/{endpoint}?access_token={self.cloud.access_token}"
        else:
            url = f"{DEFAULT_CLOUD_ADDR}/{model}{endpoint}?access_token={self.cloud.access_token}"

        return await self.request("get", url)

    async def put(
        self, model: str, endpoint: str, model_id: str, command: str, value: Any
    ) -> Any:
        """
        Put request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :param command: used for command requests. e.g. 'switchState'.
        :param value: the value to be put for the command. e.g 'switchState', 1
        :return: Dictionary with the response from the cloud.
        """
        url = (
            f"{DEFAULT_CLOUD_ADDR}/{model}/{model_id}/{endpoint}?{command}={str(value)}&access_token="
            f"{self.cloud.access_token}"
        )

        return await self.request("put", url)

    async def request(
        self, method: str, url: str, json: dict[str, Any] | None = None
    ) -> Any:
        """Make request and check data for errors."""
        async with self.client_session.request(method, url, json=json) as result:
            try:
                data: Any = await result.json()
            except ContentTypeError as err:
                # when the cloud is unavailable,
                # a payload can be received that can't be converted to a dictionary.
                raise CrownstoneConnectionError(
                    "Error connecting to the Crownstone Cloud."
                ) from err
            refresh = await self.raise_on_error(data)
            if refresh:
                new_url = url.replace(
                    url.split("access_token=", 1)[1], self.cloud.access_token
                )
                await self.request(method, new_url, json=json)
            return data

    async def raise_on_error(self, data: Any) -> bool:
        """Check for error messages and raise the correct exception."""
        if isinstance(data, dict) and "error" in data:
            error: dict[str, Any] = data["error"]
            if "code" in error:
                error_type = error["code"]
                try:
                    if error_type in ("INVALID_TOKEN", "AUTHORIZATION_REQUIRED"):
                        # Login using existing data
                        response = await self.request_login(self.cloud.login_data)
                        self.cloud.access_token = response["id"]
                        return True  # re-run the request

                    for err_type, message in AuthError.items():
                        if err_type == error_type:
                            raise CrownstoneAuthenticationError(err_type, message)

                except ValueError as err:
                    raise CrownstoneUnknownError("Unknown error occurred.") from err
            else:
                _LOGGER.error(error["message"])

        return False
