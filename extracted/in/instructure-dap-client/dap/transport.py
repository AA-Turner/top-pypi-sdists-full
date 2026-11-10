import logging
import typing
from http import HTTPStatus
from typing import Any, Mapping, Type, TypeVar, Union

import aiohttp
from aiohttp_retry import RetryClient
from strong_typing.serialization import json_dump_string, json_to_object, object_to_json

from .dap_error import (
    AccountDisabledError,
    AccountNotOnboardedError,
    AccountUnderMaintenanceError,
    AuthenticationError,
    AuthorizationFailedError,
    NotFoundError,
    OutOfRangeError,
    ProcessingError,
    RequestTypeForbiddenError,
    ServerError,
    SnapshotRequiredError,
    ValidationError,
)
from .http_json import read_json_body

logger = logging.getLogger("dap")

T = TypeVar("T")


class Transport:
    """
    Sends GET/POST requests to the DAP API and parses responses (or error
    bodies) into typed objects.

    Every request takes the bearer token to send as an argument, so what a
    request is authorized as is visible at the call site rather than held as
    state here.
    """

    _base_url: str
    _retry_client: RetryClient
    _headers: Mapping[str, str]

    def __init__(
        self,
        base_url: str,
        retry_client: RetryClient,
        headers: Mapping[str, str],
    ) -> None:
        self._base_url = base_url
        self._retry_client = retry_client
        self._headers = headers

    async def get(
        self,
        path: str,
        response_type: Type[T],
        bearer_token: str,
    ) -> T:
        """
        Sends a request to the server and parses the response into the expected type.

        :param path: The path component of the endpoint to invoke.
        :param response_type: The object type the endpoint returns on success.
        :param bearer_token: The access token to authorize the request with.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        url = f"{self._base_url}{path}"
        logger.debug(f"GET request to {url}")

        async with self._retry_client.get(
            url,
            headers={**self._headers, "Authorization": f"Bearer {bearer_token}"},
        ) as response:
            return await self._process(response, response_type)

    async def post(
        self,
        path: str,
        request_data: Any,
        response_type: Type[T],
        bearer_token: str,
    ) -> T:
        """
        Sends a request to the server by serializing a payload object, and parses the response into the expected type.

        :param path: The path component of the endpoint to invoke.
        :param request_data: The object to pass in the request body.
        :param response_type: The object type the endpoint returns on success.
        :param bearer_token: The access token to authorize the request with.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        request_payload = object_to_json(request_data)
        url = f"{self._base_url}{path}"
        logger.debug(f"POST request to {url}")
        logger.debug(f"POST request payload:\n{repr(request_payload)}")

        async with self._retry_client.post(
            url,
            data=json_dump_string(request_payload),
            headers={
                "Content-Type": "application/json",
                **self._headers,
                "Authorization": f"Bearer {bearer_token}",
            },
        ) as response:
            return await self._process(response, response_type)

    @typing.no_type_check  # mypy shits itself on Union type used in json_to_object
    def _map_to_error_type(
        self, status_code: int, response_body: Any
    ) -> Union[
        ValidationError,
        NotFoundError,
        OutOfRangeError,
        SnapshotRequiredError,
        AuthenticationError,
        AccountDisabledError,
        AccountNotOnboardedError,
        AccountUnderMaintenanceError,
        ProcessingError,
        ServerError,
    ]:
        """
        Maps error body and status to Python error object.
        """

        if "error" not in response_body:
            return ServerError(status_code, response_body)

        response_body_error = response_body["error"]

        try:
            if status_code == HTTPStatus.UNAUTHORIZED.value:
                return json_to_object(AuthenticationError, response_body_error)
            elif status_code == HTTPStatus.FORBIDDEN.value:
                return json_to_object(
                    Union[
                        AuthorizationFailedError,
                        AccountDisabledError,
                        AccountNotOnboardedError,
                        AccountUnderMaintenanceError,
                        RequestTypeForbiddenError,
                    ],
                    response_body_error,
                )
            else:
                return json_to_object(
                    Union[
                        ValidationError,
                        NotFoundError,
                        OutOfRangeError,
                        SnapshotRequiredError,
                        ProcessingError,
                    ],
                    response_body_error,
                )
        except Exception:
            return ServerError(status_code, response_body_error)

    async def _process(
        self,
        response: aiohttp.ClientResponse,
        response_type: Type[T],
    ) -> T:
        """
        Extracts an object instance from a DAP API response body.
        """

        response_payload = await read_json_body(response)
        logger.debug(f"GET/POST response payload:\n{repr(response_payload)}")

        # HTTP status codes between 400 (inclusive) and 600 (exclusive) indicate an error
        # (includes non-standard 5xx server-side error codes)
        if HTTPStatus.BAD_REQUEST.value <= response.status < 600:
            error_object = self._map_to_error_type(response.status, response_payload)
            logger.warning(f"Received error in response: {error_object}")
            raise error_object
        else:
            return json_to_object(response_type, response_payload)
