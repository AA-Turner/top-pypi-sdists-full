from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_dev_workspace_response_200 import GetDevWorkspaceResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/get_dev_workspace".format(
            workspace=workspace,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Optional[GetDevWorkspaceResponse200]]:
    if response.status_code == HTTPStatus.OK:
        _response_200 = response.json()
        response_200: Optional[GetDevWorkspaceResponse200]
        if _response_200 is None:
            response_200 = None
        else:
            response_200 = GetDevWorkspaceResponse200.from_dict(_response_200)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Optional[GetDevWorkspaceResponse200]]:
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
) -> Response[Optional[GetDevWorkspaceResponse200]]:
    """this workspace's active canonical dev workspace, if any

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetDevWorkspaceResponse200]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetDevWorkspaceResponse200]]:
    """this workspace's active canonical dev workspace, if any

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetDevWorkspaceResponse200]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[GetDevWorkspaceResponse200]]:
    """this workspace's active canonical dev workspace, if any

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetDevWorkspaceResponse200]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetDevWorkspaceResponse200]]:
    """this workspace's active canonical dev workspace, if any

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetDevWorkspaceResponse200]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
        )
    ).parsed
