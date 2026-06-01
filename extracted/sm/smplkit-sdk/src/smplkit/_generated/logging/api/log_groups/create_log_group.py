from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.log_group_create_request import LogGroupCreateRequest
from ...models.log_group_response import LogGroupResponse


def _get_kwargs(
    *,
    body: LogGroupCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/log_groups",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | LogGroupResponse | None:
    if response.status_code == 201:
        response_201 = LogGroupResponse.from_dict(response.json())

        return response_201

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
) -> Response[ErrorResponse | LogGroupResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LogGroupCreateRequest,
) -> Response[ErrorResponse | LogGroupResponse]:
    """Create Log Group

     Create a log group.

    The caller supplies the log group's key as `data.id`. The id is
    required, must be unique within the account across loggers and
    groups, and is immutable for the lifetime of the group.

    Args:
        body (LogGroupCreateRequest): JSON:API request envelope for creating a log group.

            Distinct from :class:`LogGroupRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LogGroupResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: LogGroupCreateRequest,
) -> ErrorResponse | LogGroupResponse | None:
    """Create Log Group

     Create a log group.

    The caller supplies the log group's key as `data.id`. The id is
    required, must be unique within the account across loggers and
    groups, and is immutable for the lifetime of the group.

    Args:
        body (LogGroupCreateRequest): JSON:API request envelope for creating a log group.

            Distinct from :class:`LogGroupRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LogGroupResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LogGroupCreateRequest,
) -> Response[ErrorResponse | LogGroupResponse]:
    """Create Log Group

     Create a log group.

    The caller supplies the log group's key as `data.id`. The id is
    required, must be unique within the account across loggers and
    groups, and is immutable for the lifetime of the group.

    Args:
        body (LogGroupCreateRequest): JSON:API request envelope for creating a log group.

            Distinct from :class:`LogGroupRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LogGroupResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: LogGroupCreateRequest,
) -> ErrorResponse | LogGroupResponse | None:
    """Create Log Group

     Create a log group.

    The caller supplies the log group's key as `data.id`. The id is
    required, must be unique within the account across loggers and
    groups, and is immutable for the lifetime of the group.

    Args:
        body (LogGroupCreateRequest): JSON:API request envelope for creating a log group.

            Distinct from :class:`LogGroupRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LogGroupResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
