from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.logger_request import LoggerRequest
from ...models.logger_response import LoggerResponse


def _get_kwargs(
    id: str,
    *,
    body: LoggerRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/loggers/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | LoggerResponse | None:
    if response.status_code == 200:
        response_200 = LoggerResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | LoggerResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: LoggerRequest,
) -> Response[ErrorResponse | LoggerResponse]:
    """Update or Create Logger

     Create or replace a logger at the given key.

    If the logger does not yet exist, it is created. Fields omitted from
    the request body are preserved; explicit `null` clears them. Setting
    `level`, `group`, or `environments` on an unmanaged logger promotes
    it to managed automatically.

    Args:
        id (str):
        body (LoggerRequest): JSON:API request envelope for creating or updating a logger.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LoggerResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: LoggerRequest,
) -> ErrorResponse | LoggerResponse | None:
    """Update or Create Logger

     Create or replace a logger at the given key.

    If the logger does not yet exist, it is created. Fields omitted from
    the request body are preserved; explicit `null` clears them. Setting
    `level`, `group`, or `environments` on an unmanaged logger promotes
    it to managed automatically.

    Args:
        id (str):
        body (LoggerRequest): JSON:API request envelope for creating or updating a logger.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LoggerResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: LoggerRequest,
) -> Response[ErrorResponse | LoggerResponse]:
    """Update or Create Logger

     Create or replace a logger at the given key.

    If the logger does not yet exist, it is created. Fields omitted from
    the request body are preserved; explicit `null` clears them. Setting
    `level`, `group`, or `environments` on an unmanaged logger promotes
    it to managed automatically.

    Args:
        id (str):
        body (LoggerRequest): JSON:API request envelope for creating or updating a logger.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LoggerResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: LoggerRequest,
) -> ErrorResponse | LoggerResponse | None:
    """Update or Create Logger

     Create or replace a logger at the given key.

    If the logger does not yet exist, it is created. Fields omitted from
    the request body are preserved; explicit `null` clears them. Setting
    `level`, `group`, or `environments` on an unmanaged logger promotes
    it to managed automatically.

    Args:
        id (str):
        body (LoggerRequest): JSON:API request envelope for creating or updating a logger.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LoggerResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
