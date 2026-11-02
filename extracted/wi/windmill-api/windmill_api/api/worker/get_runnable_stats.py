from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_runnable_stats_order_by import GetRunnableStatsOrderBy
from ...models.get_runnable_stats_response_200_item import GetRunnableStatsResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    window_secs: Union[Unset, None, int] = UNSET,
    worker_group: Union[Unset, None, str] = UNSET,
    workspace: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetRunnableStatsOrderBy] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["window_secs"] = window_secs

    params["worker_group"] = worker_group

    params["workspace"] = workspace

    json_order_by: Union[Unset, None, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value if order_by else None

    params["order_by"] = json_order_by

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/workers/runnable_stats",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["GetRunnableStatsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetRunnableStatsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["GetRunnableStatsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
    worker_group: Union[Unset, None, str] = UNSET,
    workspace: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetRunnableStatsOrderBy] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[List["GetRunnableStatsResponse200Item"]]:
    """get resource usage per runnable and worker group over a time window (require devops role)

    Args:
        window_secs (Union[Unset, None, int]):
        worker_group (Union[Unset, None, str]):
        workspace (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetRunnableStatsOrderBy]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetRunnableStatsResponse200Item']]
    """

    kwargs = _get_kwargs(
        window_secs=window_secs,
        worker_group=worker_group,
        workspace=workspace,
        order_by=order_by,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
    worker_group: Union[Unset, None, str] = UNSET,
    workspace: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetRunnableStatsOrderBy] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[List["GetRunnableStatsResponse200Item"]]:
    """get resource usage per runnable and worker group over a time window (require devops role)

    Args:
        window_secs (Union[Unset, None, int]):
        worker_group (Union[Unset, None, str]):
        workspace (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetRunnableStatsOrderBy]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetRunnableStatsResponse200Item']
    """

    return sync_detailed(
        client=client,
        window_secs=window_secs,
        worker_group=worker_group,
        workspace=workspace,
        order_by=order_by,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
    worker_group: Union[Unset, None, str] = UNSET,
    workspace: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetRunnableStatsOrderBy] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[List["GetRunnableStatsResponse200Item"]]:
    """get resource usage per runnable and worker group over a time window (require devops role)

    Args:
        window_secs (Union[Unset, None, int]):
        worker_group (Union[Unset, None, str]):
        workspace (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetRunnableStatsOrderBy]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['GetRunnableStatsResponse200Item']]
    """

    kwargs = _get_kwargs(
        window_secs=window_secs,
        worker_group=worker_group,
        workspace=workspace,
        order_by=order_by,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    window_secs: Union[Unset, None, int] = UNSET,
    worker_group: Union[Unset, None, str] = UNSET,
    workspace: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, GetRunnableStatsOrderBy] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[List["GetRunnableStatsResponse200Item"]]:
    """get resource usage per runnable and worker group over a time window (require devops role)

    Args:
        window_secs (Union[Unset, None, int]):
        worker_group (Union[Unset, None, str]):
        workspace (Union[Unset, None, str]):
        order_by (Union[Unset, None, GetRunnableStatsOrderBy]):
        limit (Union[Unset, None, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['GetRunnableStatsResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
            window_secs=window_secs,
            worker_group=worker_group,
            workspace=workspace,
            order_by=order_by,
            limit=limit,
        )
    ).parsed
