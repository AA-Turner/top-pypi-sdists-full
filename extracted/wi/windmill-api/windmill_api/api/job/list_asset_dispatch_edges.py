import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_asset_dispatch_edges_response_200_item import ListAssetDispatchEdgesResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    path_start: str,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["path_start"] = path_start

    json_created_after: Union[Unset, None, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat() if created_after else None

    params["created_after"] = json_created_after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/asset_dispatch_edges".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListAssetDispatchEdgesResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListAssetDispatchEdgesResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListAssetDispatchEdgesResponse200Item"]]:
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
    path_start: str,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[List["ListAssetDispatchEdgesResponse200Item"]]:
    """list asset-cascade producer→child job edges for a folder

     Returns the `dispatched` asset-trigger edges (producer job → child job) whose subscriber lives under
    `path_start`. Lets a pipeline view reconstruct the cascade tree of a folder by job id and group
    connected runs. Visibility follows the producer job's RLS.

    Args:
        workspace (str):
        path_start (str):
        created_after (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAssetDispatchEdgesResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path_start=path_start,
        created_after=created_after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path_start: str,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[List["ListAssetDispatchEdgesResponse200Item"]]:
    """list asset-cascade producer→child job edges for a folder

     Returns the `dispatched` asset-trigger edges (producer job → child job) whose subscriber lives under
    `path_start`. Lets a pipeline view reconstruct the cascade tree of a folder by job id and group
    connected runs. Visibility follows the producer job's RLS.

    Args:
        workspace (str):
        path_start (str):
        created_after (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAssetDispatchEdgesResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        path_start=path_start,
        created_after=created_after,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path_start: str,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[List["ListAssetDispatchEdgesResponse200Item"]]:
    """list asset-cascade producer→child job edges for a folder

     Returns the `dispatched` asset-trigger edges (producer job → child job) whose subscriber lives under
    `path_start`. Lets a pipeline view reconstruct the cascade tree of a folder by job id and group
    connected runs. Visibility follows the producer job's RLS.

    Args:
        workspace (str):
        path_start (str):
        created_after (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListAssetDispatchEdgesResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path_start=path_start,
        created_after=created_after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path_start: str,
    created_after: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[List["ListAssetDispatchEdgesResponse200Item"]]:
    """list asset-cascade producer→child job edges for a folder

     Returns the `dispatched` asset-trigger edges (producer job → child job) whose subscriber lives under
    `path_start`. Lets a pipeline view reconstruct the cascade tree of a folder by job id and group
    connected runs. Visibility follows the producer job's RLS.

    Args:
        workspace (str):
        path_start (str):
        created_after (Union[Unset, None, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListAssetDispatchEdgesResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            path_start=path_start,
            created_after=created_after,
        )
    ).parsed
