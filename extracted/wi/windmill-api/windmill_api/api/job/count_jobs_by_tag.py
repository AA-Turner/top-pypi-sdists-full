from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.count_jobs_by_tag_response_200_item import CountJobsByTagResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    horizon_secs: Union[Unset, None, int] = UNSET,
    workspace_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["horizon_secs"] = horizon_secs

    params["workspace_id"] = workspace_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/jobs/completed/count_by_tag",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["CountJobsByTagResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CountJobsByTagResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["CountJobsByTagResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    horizon_secs: Union[Unset, None, int] = UNSET,
    workspace_id: Union[Unset, None, str] = UNSET,
) -> Response[List["CountJobsByTagResponse200Item"]]:
    """Count jobs by tag

    Args:
        horizon_secs (Union[Unset, None, int]):
        workspace_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['CountJobsByTagResponse200Item']]
    """

    kwargs = _get_kwargs(
        horizon_secs=horizon_secs,
        workspace_id=workspace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    horizon_secs: Union[Unset, None, int] = UNSET,
    workspace_id: Union[Unset, None, str] = UNSET,
) -> Optional[List["CountJobsByTagResponse200Item"]]:
    """Count jobs by tag

    Args:
        horizon_secs (Union[Unset, None, int]):
        workspace_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['CountJobsByTagResponse200Item']
    """

    return sync_detailed(
        client=client,
        horizon_secs=horizon_secs,
        workspace_id=workspace_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    horizon_secs: Union[Unset, None, int] = UNSET,
    workspace_id: Union[Unset, None, str] = UNSET,
) -> Response[List["CountJobsByTagResponse200Item"]]:
    """Count jobs by tag

    Args:
        horizon_secs (Union[Unset, None, int]):
        workspace_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['CountJobsByTagResponse200Item']]
    """

    kwargs = _get_kwargs(
        horizon_secs=horizon_secs,
        workspace_id=workspace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    horizon_secs: Union[Unset, None, int] = UNSET,
    workspace_id: Union[Unset, None, str] = UNSET,
) -> Optional[List["CountJobsByTagResponse200Item"]]:
    """Count jobs by tag

    Args:
        horizon_secs (Union[Unset, None, int]):
        workspace_id (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['CountJobsByTagResponse200Item']
    """

    return (
        await asyncio_detailed(
            client=client,
            horizon_secs=horizon_secs,
            workspace_id=workspace_id,
        )
    ).parsed
