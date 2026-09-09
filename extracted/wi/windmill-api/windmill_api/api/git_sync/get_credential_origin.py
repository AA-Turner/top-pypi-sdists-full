from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_credential_origin_response_200 import GetCredentialOriginResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    path: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/git_sync/credential/origin".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetCredentialOriginResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetCredentialOriginResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetCredentialOriginResponse200]:
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
    path: str,
) -> Response[GetCredentialOriginResponse200]:
    """Where a repository's credential comes from

     Whether Windmill holds this repository's access token, and which host it talks to. `held` means this
    workspace stores it, `borrowed` means an ancestor does and it is not this workspace's to replace.
    Both absent means the repository authenticates with whatever its URL carries. Returns no secret.
    Requires workspace admin.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetCredentialOriginResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Optional[GetCredentialOriginResponse200]:
    """Where a repository's credential comes from

     Whether Windmill holds this repository's access token, and which host it talks to. `held` means this
    workspace stores it, `borrowed` means an ancestor does and it is not this workspace's to replace.
    Both absent means the repository authenticates with whatever its URL carries. Returns no secret.
    Requires workspace admin.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetCredentialOriginResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        path=path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Response[GetCredentialOriginResponse200]:
    """Where a repository's credential comes from

     Whether Windmill holds this repository's access token, and which host it talks to. `held` means this
    workspace stores it, `borrowed` means an ancestor does and it is not this workspace's to replace.
    Both absent means the repository authenticates with whatever its URL carries. Returns no secret.
    Requires workspace admin.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetCredentialOriginResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Optional[GetCredentialOriginResponse200]:
    """Where a repository's credential comes from

     Whether Windmill holds this repository's access token, and which host it talks to. `held` means this
    workspace stores it, `borrowed` means an ancestor does and it is not this workspace's to replace.
    Both absent means the repository authenticates with whatever its URL carries. Returns no secret.
    Requires workspace admin.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetCredentialOriginResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            path=path,
        )
    ).parsed
