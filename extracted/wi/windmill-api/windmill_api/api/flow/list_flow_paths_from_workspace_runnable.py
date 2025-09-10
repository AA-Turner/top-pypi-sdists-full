from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_flow_paths_from_workspace_runnable_runnable_kind import (
    ListFlowPathsFromWorkspaceRunnableRunnableKind,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    runnable_kind: ListFlowPathsFromWorkspaceRunnableRunnableKind,
    path: str,
    *,
    match_path_start: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["match_path_start"] = match_path_start

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/flows/list_paths_from_workspace_runnable/{runnable_kind}/{path}".format(
            workspace=workspace,
            runnable_kind=runnable_kind,
            path=path,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[str], response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    runnable_kind: ListFlowPathsFromWorkspaceRunnableRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    match_path_start: Union[Unset, None, bool] = UNSET,
) -> Response[List[str]]:
    """list flow paths from workspace runnable

    Args:
        workspace (str):
        runnable_kind (ListFlowPathsFromWorkspaceRunnableRunnableKind):
        path (str):
        match_path_start (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        match_path_start=match_path_start,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    runnable_kind: ListFlowPathsFromWorkspaceRunnableRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    match_path_start: Union[Unset, None, bool] = UNSET,
) -> Optional[List[str]]:
    """list flow paths from workspace runnable

    Args:
        workspace (str):
        runnable_kind (ListFlowPathsFromWorkspaceRunnableRunnableKind):
        path (str):
        match_path_start (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return sync_detailed(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        client=client,
        match_path_start=match_path_start,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    runnable_kind: ListFlowPathsFromWorkspaceRunnableRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    match_path_start: Union[Unset, None, bool] = UNSET,
) -> Response[List[str]]:
    """list flow paths from workspace runnable

    Args:
        workspace (str):
        runnable_kind (ListFlowPathsFromWorkspaceRunnableRunnableKind):
        path (str):
        match_path_start (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        match_path_start=match_path_start,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    runnable_kind: ListFlowPathsFromWorkspaceRunnableRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    match_path_start: Union[Unset, None, bool] = UNSET,
) -> Optional[List[str]]:
    """list flow paths from workspace runnable

    Args:
        workspace (str):
        runnable_kind (ListFlowPathsFromWorkspaceRunnableRunnableKind):
        path (str):
        match_path_start (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            runnable_kind=runnable_kind,
            path=path,
            client=client,
            match_path_start=match_path_start,
        )
    ).parsed
