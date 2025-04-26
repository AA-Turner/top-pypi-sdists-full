from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_queue_count_response_200 import GetQueueCountResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["all_workspaces"] = all_workspaces

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/queue/count".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetQueueCountResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetQueueCountResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetQueueCountResponse200]:
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
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Response[GetQueueCountResponse200]:
    """get queue count

    Args:
        workspace (str):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetQueueCountResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        all_workspaces=all_workspaces,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Optional[GetQueueCountResponse200]:
    """get queue count

    Args:
        workspace (str):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetQueueCountResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        all_workspaces=all_workspaces,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Response[GetQueueCountResponse200]:
    """get queue count

    Args:
        workspace (str):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetQueueCountResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        all_workspaces=all_workspaces,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Optional[GetQueueCountResponse200]:
    """get queue count

    Args:
        workspace (str):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetQueueCountResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            all_workspaces=all_workspaces,
        )
    ).parsed
