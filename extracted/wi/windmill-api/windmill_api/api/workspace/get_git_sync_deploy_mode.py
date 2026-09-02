from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_git_sync_deploy_mode_response_200 import GetGitSyncDeployModeResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    branch: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["branch"] = branch

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/git_sync_deploy_mode".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetGitSyncDeployModeResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetGitSyncDeployModeResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetGitSyncDeployModeResponse200]:
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
    branch: Union[Unset, None, str] = UNSET,
) -> Response[GetGitSyncDeployModeResponse200]:
    """Get how local changes deploy to this workspace via git sync

    Args:
        workspace (str):
        branch (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGitSyncDeployModeResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        branch=branch,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    branch: Union[Unset, None, str] = UNSET,
) -> Optional[GetGitSyncDeployModeResponse200]:
    """Get how local changes deploy to this workspace via git sync

    Args:
        workspace (str):
        branch (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetGitSyncDeployModeResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        branch=branch,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    branch: Union[Unset, None, str] = UNSET,
) -> Response[GetGitSyncDeployModeResponse200]:
    """Get how local changes deploy to this workspace via git sync

    Args:
        workspace (str):
        branch (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGitSyncDeployModeResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        branch=branch,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    branch: Union[Unset, None, str] = UNSET,
) -> Optional[GetGitSyncDeployModeResponse200]:
    """Get how local changes deploy to this workspace via git sync

    Args:
        workspace (str):
        branch (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetGitSyncDeployModeResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            branch=branch,
        )
    ).parsed
