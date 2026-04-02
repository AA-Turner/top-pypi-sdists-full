from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.remote_resource_sync_status import RemoteResourceSyncStatus
from ...types import Response


def _get_kwargs(
    resource_uuid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/remote-waldur-api/remote_resource_status/{resource_uuid}/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> RemoteResourceSyncStatus:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = RemoteResourceSyncStatus.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RemoteResourceSyncStatus]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[RemoteResourceSyncStatus]:
    """Get remote resource sync status

    Args:
        resource_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoteResourceSyncStatus]
    """

    kwargs = _get_kwargs(
        resource_uuid=resource_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_uuid: str,
    *,
    client: AuthenticatedClient,
) -> RemoteResourceSyncStatus:
    """Get remote resource sync status

    Args:
        resource_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoteResourceSyncStatus
    """

    return sync_detailed(
        resource_uuid=resource_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    resource_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[RemoteResourceSyncStatus]:
    """Get remote resource sync status

    Args:
        resource_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoteResourceSyncStatus]
    """

    kwargs = _get_kwargs(
        resource_uuid=resource_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_uuid: str,
    *,
    client: AuthenticatedClient,
) -> RemoteResourceSyncStatus:
    """Get remote resource sync status

    Args:
        resource_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoteResourceSyncStatus
    """

    return (
        await asyncio_detailed(
            resource_uuid=resource_uuid,
            client=client,
        )
    ).parsed
