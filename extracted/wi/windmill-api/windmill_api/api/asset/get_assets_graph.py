from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_assets_graph_response_200 import GetAssetsGraphResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["asset_kinds"] = asset_kinds

    params["folder"] = folder

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/assets/graph".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetAssetsGraphResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAssetsGraphResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetAssetsGraphResponse200]:
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
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
) -> Response[GetAssetsGraphResponse200]:
    """Get the workspace-wide asset <-> runnable graph

    Args:
        workspace (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAssetsGraphResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        asset_kinds=asset_kinds,
        folder=folder,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
) -> Optional[GetAssetsGraphResponse200]:
    """Get the workspace-wide asset <-> runnable graph

    Args:
        workspace (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAssetsGraphResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        asset_kinds=asset_kinds,
        folder=folder,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
) -> Response[GetAssetsGraphResponse200]:
    """Get the workspace-wide asset <-> runnable graph

    Args:
        workspace (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAssetsGraphResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        asset_kinds=asset_kinds,
        folder=folder,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    asset_kinds: Union[Unset, None, str] = UNSET,
    folder: Union[Unset, None, str] = UNSET,
) -> Optional[GetAssetsGraphResponse200]:
    """Get the workspace-wide asset <-> runnable graph

    Args:
        workspace (str):
        asset_kinds (Union[Unset, None, str]):
        folder (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAssetsGraphResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            asset_kinds=asset_kinds,
            folder=folder,
        )
    ).parsed
