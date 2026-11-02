from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_storage_usage_response_200 import GetStorageUsageResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    refresh: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["refresh"] = refresh

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/storage_usage".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetStorageUsageResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetStorageUsageResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetStorageUsageResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    refresh: Union[Unset, None, bool] = UNSET,
) -> Response[GetStorageUsageResponse200]:
    """Get the storage usage of the workspace object storage, per configured storage. On Community Edition,
    also returns the workspace storage quota.

    Args:
        workspace (str):
        refresh (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetStorageUsageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        refresh=refresh,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    refresh: Union[Unset, None, bool] = UNSET,
) -> Optional[GetStorageUsageResponse200]:
    """Get the storage usage of the workspace object storage, per configured storage. On Community Edition,
    also returns the workspace storage quota.

    Args:
        workspace (str):
        refresh (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetStorageUsageResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        refresh=refresh,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    refresh: Union[Unset, None, bool] = UNSET,
) -> Response[GetStorageUsageResponse200]:
    """Get the storage usage of the workspace object storage, per configured storage. On Community Edition,
    also returns the workspace storage quota.

    Args:
        workspace (str):
        refresh (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetStorageUsageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        refresh=refresh,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    refresh: Union[Unset, None, bool] = UNSET,
) -> Optional[GetStorageUsageResponse200]:
    """Get the storage usage of the workspace object storage, per configured storage. On Community Edition,
    also returns the workspace storage quota.

    Args:
        workspace (str):
        refresh (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetStorageUsageResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            refresh=refresh,
        )
    ).parsed
