from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_principal_access_response_200 import GetPrincipalAccessResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    principal: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["principal"] = principal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/access/get".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetPrincipalAccessResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetPrincipalAccessResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetPrincipalAccessResponse200]:
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
    principal: str,
) -> Response[GetPrincipalAccessResponse200]:
    """list what a workspace member or group can reach, and why

     Workspace admins can query any principal; other members only themselves and the groups
    they belong to. An admin principal reaches everything, so `items` is empty.

    Args:
        workspace (str):
        principal (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPrincipalAccessResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        principal=principal,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    principal: str,
) -> Optional[GetPrincipalAccessResponse200]:
    """list what a workspace member or group can reach, and why

     Workspace admins can query any principal; other members only themselves and the groups
    they belong to. An admin principal reaches everything, so `items` is empty.

    Args:
        workspace (str):
        principal (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPrincipalAccessResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        principal=principal,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    principal: str,
) -> Response[GetPrincipalAccessResponse200]:
    """list what a workspace member or group can reach, and why

     Workspace admins can query any principal; other members only themselves and the groups
    they belong to. An admin principal reaches everything, so `items` is empty.

    Args:
        workspace (str):
        principal (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetPrincipalAccessResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        principal=principal,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    principal: str,
) -> Optional[GetPrincipalAccessResponse200]:
    """list what a workspace member or group can reach, and why

     Workspace admins can query any principal; other members only themselves and the groups
    they belong to. An admin principal reaches everything, so `items` is empty.

    Args:
        workspace (str):
        principal (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetPrincipalAccessResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            principal=principal,
        )
    ).parsed
