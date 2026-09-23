from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_remote_deploy_target_response_200 import GetRemoteDeployTargetResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/remote_deploy/target".format(
            workspace=workspace,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetRemoteDeployTargetResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetRemoteDeployTargetResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetRemoteDeployTargetResponse200]:
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
) -> Response[GetRemoteDeployTargetResponse200]:
    """get the workspace's deploy target on another instance, and the caller's connection to it

     Once connected, deploy calls aimed at the target go through
    `/w/{workspace}/remote_deploy/proxy/{proxy_key}/{route}`, which forwards any method to
    `{base_url}/api/w/{target workspace}/{route}` with the caller's stored token.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetRemoteDeployTargetResponse200]
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
) -> Optional[GetRemoteDeployTargetResponse200]:
    """get the workspace's deploy target on another instance, and the caller's connection to it

     Once connected, deploy calls aimed at the target go through
    `/w/{workspace}/remote_deploy/proxy/{proxy_key}/{route}`, which forwards any method to
    `{base_url}/api/w/{target workspace}/{route}` with the caller's stored token.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetRemoteDeployTargetResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetRemoteDeployTargetResponse200]:
    """get the workspace's deploy target on another instance, and the caller's connection to it

     Once connected, deploy calls aimed at the target go through
    `/w/{workspace}/remote_deploy/proxy/{proxy_key}/{route}`, which forwards any method to
    `{base_url}/api/w/{target workspace}/{route}` with the caller's stored token.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetRemoteDeployTargetResponse200]
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
) -> Optional[GetRemoteDeployTargetResponse200]:
    """get the workspace's deploy target on another instance, and the caller's connection to it

     Once connected, deploy calls aimed at the target go through
    `/w/{workspace}/remote_deploy/proxy/{proxy_key}/{route}`, which forwards any method to
    `{base_url}/api/w/{target workspace}/{route}` with the caller's stored token.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetRemoteDeployTargetResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
        )
    ).parsed
