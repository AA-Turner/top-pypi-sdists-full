from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.flag_create_request import FlagCreateRequest
from ...models.flag_response import FlagResponse


def _get_kwargs(
    *,
    body: FlagCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/flags",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FlagResponse | None:
    if response.status_code == 201:
        response_201 = FlagResponse.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FlagResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FlagCreateRequest,
) -> Response[FlagResponse]:
    """Create Flag

     Create a new feature flag. The caller provides the id (the flag key) in the request body.

    Args:
        body (FlagCreateRequest): JSON:API request envelope for creating a flag.

            Distinct from :class:`FlagRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlagResponse]
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
    body: FlagCreateRequest,
) -> FlagResponse | None:
    """Create Flag

     Create a new feature flag. The caller provides the id (the flag key) in the request body.

    Args:
        body (FlagCreateRequest): JSON:API request envelope for creating a flag.

            Distinct from :class:`FlagRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlagResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FlagCreateRequest,
) -> Response[FlagResponse]:
    """Create Flag

     Create a new feature flag. The caller provides the id (the flag key) in the request body.

    Args:
        body (FlagCreateRequest): JSON:API request envelope for creating a flag.

            Distinct from :class:`FlagRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlagResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FlagCreateRequest,
) -> FlagResponse | None:
    """Create Flag

     Create a new feature flag. The caller provides the id (the flag key) in the request body.

    Args:
        body (FlagCreateRequest): JSON:API request envelope for creating a flag.

            Distinct from :class:`FlagRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlagResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
