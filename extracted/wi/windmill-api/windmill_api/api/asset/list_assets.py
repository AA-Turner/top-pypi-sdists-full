import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_assets_response_200 import ListAssetsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    per_page: Union[Unset, None, int] = 50,
    cursor_created_at: Union[Unset, None, datetime.datetime] = UNSET,
    cursor_id: Union[Unset, None, int] = UNSET,
    asset_path: Union[Unset, None, str] = UNSET,
    usage_path: Union[Unset, None, str] = UNSET,
    asset_kinds: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["per_page"] = per_page

    json_cursor_created_at: Union[Unset, None, str] = UNSET
    if not isinstance(cursor_created_at, Unset):
        json_cursor_created_at = cursor_created_at.isoformat() if cursor_created_at else None

    params["cursor_created_at"] = json_cursor_created_at

    params["cursor_id"] = cursor_id

    params["asset_path"] = asset_path

    params["usage_path"] = usage_path

    params["asset_kinds"] = asset_kinds

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/assets/list".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListAssetsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAssetsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListAssetsResponse200]:
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
    per_page: Union[Unset, None, int] = 50,
    cursor_created_at: Union[Unset, None, datetime.datetime] = UNSET,
    cursor_id: Union[Unset, None, int] = UNSET,
    asset_path: Union[Unset, None, str] = UNSET,
    usage_path: Union[Unset, None, str] = UNSET,
    asset_kinds: Union[Unset, None, str] = UNSET,
) -> Response[ListAssetsResponse200]:
    """List all assets in the workspace with cursor pagination

    Args:
        workspace (str):
        per_page (Union[Unset, None, int]):  Default: 50.
        cursor_created_at (Union[Unset, None, datetime.datetime]):
        cursor_id (Union[Unset, None, int]):
        asset_path (Union[Unset, None, str]):
        usage_path (Union[Unset, None, str]):
        asset_kinds (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAssetsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        per_page=per_page,
        cursor_created_at=cursor_created_at,
        cursor_id=cursor_id,
        asset_path=asset_path,
        usage_path=usage_path,
        asset_kinds=asset_kinds,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    per_page: Union[Unset, None, int] = 50,
    cursor_created_at: Union[Unset, None, datetime.datetime] = UNSET,
    cursor_id: Union[Unset, None, int] = UNSET,
    asset_path: Union[Unset, None, str] = UNSET,
    usage_path: Union[Unset, None, str] = UNSET,
    asset_kinds: Union[Unset, None, str] = UNSET,
) -> Optional[ListAssetsResponse200]:
    """List all assets in the workspace with cursor pagination

    Args:
        workspace (str):
        per_page (Union[Unset, None, int]):  Default: 50.
        cursor_created_at (Union[Unset, None, datetime.datetime]):
        cursor_id (Union[Unset, None, int]):
        asset_path (Union[Unset, None, str]):
        usage_path (Union[Unset, None, str]):
        asset_kinds (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAssetsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        per_page=per_page,
        cursor_created_at=cursor_created_at,
        cursor_id=cursor_id,
        asset_path=asset_path,
        usage_path=usage_path,
        asset_kinds=asset_kinds,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    per_page: Union[Unset, None, int] = 50,
    cursor_created_at: Union[Unset, None, datetime.datetime] = UNSET,
    cursor_id: Union[Unset, None, int] = UNSET,
    asset_path: Union[Unset, None, str] = UNSET,
    usage_path: Union[Unset, None, str] = UNSET,
    asset_kinds: Union[Unset, None, str] = UNSET,
) -> Response[ListAssetsResponse200]:
    """List all assets in the workspace with cursor pagination

    Args:
        workspace (str):
        per_page (Union[Unset, None, int]):  Default: 50.
        cursor_created_at (Union[Unset, None, datetime.datetime]):
        cursor_id (Union[Unset, None, int]):
        asset_path (Union[Unset, None, str]):
        usage_path (Union[Unset, None, str]):
        asset_kinds (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAssetsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        per_page=per_page,
        cursor_created_at=cursor_created_at,
        cursor_id=cursor_id,
        asset_path=asset_path,
        usage_path=usage_path,
        asset_kinds=asset_kinds,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    per_page: Union[Unset, None, int] = 50,
    cursor_created_at: Union[Unset, None, datetime.datetime] = UNSET,
    cursor_id: Union[Unset, None, int] = UNSET,
    asset_path: Union[Unset, None, str] = UNSET,
    usage_path: Union[Unset, None, str] = UNSET,
    asset_kinds: Union[Unset, None, str] = UNSET,
) -> Optional[ListAssetsResponse200]:
    """List all assets in the workspace with cursor pagination

    Args:
        workspace (str):
        per_page (Union[Unset, None, int]):  Default: 50.
        cursor_created_at (Union[Unset, None, datetime.datetime]):
        cursor_id (Union[Unset, None, int]):
        asset_path (Union[Unset, None, str]):
        usage_path (Union[Unset, None, str]):
        asset_kinds (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAssetsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            per_page=per_page,
            cursor_created_at=cursor_created_at,
            cursor_id=cursor_id,
            asset_path=asset_path,
            usage_path=usage_path,
            asset_kinds=asset_kinds,
        )
    ).parsed
