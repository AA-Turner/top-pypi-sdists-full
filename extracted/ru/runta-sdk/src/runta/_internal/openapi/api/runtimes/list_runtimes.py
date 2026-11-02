from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.list_runtimes_response import ListRuntimesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["status"] = status

    params["limit"] = limit

    params["after"] = after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v2/runtimes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | ListRuntimesResponse:
    if response.status_code == 200:
        response_200 = ListRuntimesResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 501:
        response_501 = ErrorEnvelope.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ErrorEnvelope.from_dict(response.json())

        return response_504

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorEnvelope | ListRuntimesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    status: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> Response[ErrorEnvelope | ListRuntimesResponse]:
    """List runtimes

    Args:
        status (str | Unset): Comma-separated public status aliases.
        limit (int | Unset): Maximum number of runtimes to return. Default: 50.
        after (str | Unset): Opaque cursor returned by the previous page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | ListRuntimesResponse]
    """

    kwargs = _get_kwargs(
        status=status,
        limit=limit,
        after=after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    status: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> ErrorEnvelope | ListRuntimesResponse | None:
    """List runtimes

    Args:
        status (str | Unset): Comma-separated public status aliases.
        limit (int | Unset): Maximum number of runtimes to return. Default: 50.
        after (str | Unset): Opaque cursor returned by the previous page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | ListRuntimesResponse
    """

    return sync_detailed(
        client=client,
        status=status,
        limit=limit,
        after=after,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    status: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> Response[ErrorEnvelope | ListRuntimesResponse]:
    """List runtimes

    Args:
        status (str | Unset): Comma-separated public status aliases.
        limit (int | Unset): Maximum number of runtimes to return. Default: 50.
        after (str | Unset): Opaque cursor returned by the previous page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | ListRuntimesResponse]
    """

    kwargs = _get_kwargs(
        status=status,
        limit=limit,
        after=after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    status: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> ErrorEnvelope | ListRuntimesResponse | None:
    """List runtimes

    Args:
        status (str | Unset): Comma-separated public status aliases.
        limit (int | Unset): Maximum number of runtimes to return. Default: 50.
        after (str | Unset): Opaque cursor returned by the previous page.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | ListRuntimesResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            limit=limit,
            after=after,
        )
    ).parsed
