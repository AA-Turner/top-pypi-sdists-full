from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.compare_workspaces_response_200 import CompareWorkspacesResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    target_workspace_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/compare/{target_workspace_id}".format(
            workspace=workspace,
            target_workspace_id=target_workspace_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CompareWorkspacesResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CompareWorkspacesResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CompareWorkspacesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[CompareWorkspacesResponse200]:
    """Compare two workspaces

     Compares the current workspace with a target workspace to find differences in scripts, flows, apps,
    resources, and variables. Returns information about items that are ahead, behind, or in conflict.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CompareWorkspacesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        target_workspace_id=target_workspace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[CompareWorkspacesResponse200]:
    """Compare two workspaces

     Compares the current workspace with a target workspace to find differences in scripts, flows, apps,
    resources, and variables. Returns information about items that are ahead, behind, or in conflict.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CompareWorkspacesResponse200
    """

    return sync_detailed(
        workspace=workspace,
        target_workspace_id=target_workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[CompareWorkspacesResponse200]:
    """Compare two workspaces

     Compares the current workspace with a target workspace to find differences in scripts, flows, apps,
    resources, and variables. Returns information about items that are ahead, behind, or in conflict.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CompareWorkspacesResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        target_workspace_id=target_workspace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[CompareWorkspacesResponse200]:
    """Compare two workspaces

     Compares the current workspace with a target workspace to find differences in scripts, flows, apps,
    resources, and variables. Returns information about items that are ahead, behind, or in conflict.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CompareWorkspacesResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            target_workspace_id=target_workspace_id,
            client=client,
        )
    ).parsed
