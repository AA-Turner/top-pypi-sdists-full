from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sync_status_response import SyncStatusResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    offering_uuid: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["offering_uuid"] = offering_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/offering-keycloak-groups/sync_status/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> SyncStatusResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = SyncStatusResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SyncStatusResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    offering_uuid: str,
) -> Response[SyncStatusResponse]:
    """Compare local and remote Keycloak group state

    Args:
        offering_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SyncStatusResponse]
    """

    kwargs = _get_kwargs(
        offering_uuid=offering_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    offering_uuid: str,
) -> SyncStatusResponse:
    """Compare local and remote Keycloak group state

    Args:
        offering_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SyncStatusResponse
    """

    return sync_detailed(
        client=client,
        offering_uuid=offering_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    offering_uuid: str,
) -> Response[SyncStatusResponse]:
    """Compare local and remote Keycloak group state

    Args:
        offering_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SyncStatusResponse]
    """

    kwargs = _get_kwargs(
        offering_uuid=offering_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    offering_uuid: str,
) -> SyncStatusResponse:
    """Compare local and remote Keycloak group state

    Args:
        offering_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SyncStatusResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            offering_uuid=offering_uuid,
        )
    ).parsed
