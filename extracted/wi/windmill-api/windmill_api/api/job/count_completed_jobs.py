from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    completed_after_s_ago: Union[Unset, None, int] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["completed_after_s_ago"] = completed_after_s_ago

    params["success"] = success

    params["tags"] = tags

    params["all_workspaces"] = all_workspaces

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/completed/count_jobs".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[int]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(int, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
    completed_after_s_ago: Union[Unset, None, int] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Response[int]:
    """count number of completed jobs with filter

    Args:
        workspace (str):
        completed_after_s_ago (Union[Unset, None, int]):
        success (Union[Unset, None, bool]):
        tags (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        completed_after_s_ago=completed_after_s_ago,
        success=success,
        tags=tags,
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
    completed_after_s_ago: Union[Unset, None, int] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Optional[int]:
    """count number of completed jobs with filter

    Args:
        workspace (str):
        completed_after_s_ago (Union[Unset, None, int]):
        success (Union[Unset, None, bool]):
        tags (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        completed_after_s_ago=completed_after_s_ago,
        success=success,
        tags=tags,
        all_workspaces=all_workspaces,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    completed_after_s_ago: Union[Unset, None, int] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Response[int]:
    """count number of completed jobs with filter

    Args:
        workspace (str):
        completed_after_s_ago (Union[Unset, None, int]):
        success (Union[Unset, None, bool]):
        tags (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        completed_after_s_ago=completed_after_s_ago,
        success=success,
        tags=tags,
        all_workspaces=all_workspaces,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    completed_after_s_ago: Union[Unset, None, int] = UNSET,
    success: Union[Unset, None, bool] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    all_workspaces: Union[Unset, None, bool] = UNSET,
) -> Optional[int]:
    """count number of completed jobs with filter

    Args:
        workspace (str):
        completed_after_s_ago (Union[Unset, None, int]):
        success (Union[Unset, None, bool]):
        tags (Union[Unset, None, str]):
        all_workspaces (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            completed_after_s_ago=completed_after_s_ago,
            success=success,
            tags=tags,
            all_workspaces=all_workspaces,
        )
    ).parsed
