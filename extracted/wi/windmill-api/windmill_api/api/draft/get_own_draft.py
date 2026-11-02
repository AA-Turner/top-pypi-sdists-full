from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_own_draft_kind import GetOwnDraftKind
from ...models.get_own_draft_response_200 import GetOwnDraftResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    kind: GetOwnDraftKind,
    path: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/drafts/get_own/{kind}/{path}".format(
            workspace=workspace,
            kind=kind,
            path=path,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Optional[GetOwnDraftResponse200]]:
    if response.status_code == HTTPStatus.OK:
        _response_200 = response.json()
        response_200: Optional[GetOwnDraftResponse200]
        if _response_200 is None:
            response_200 = None
        else:
            response_200 = GetOwnDraftResponse200.from_dict(_response_200)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Optional[GetOwnDraftResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    kind: GetOwnDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[GetOwnDraftResponse200]]:
    """fetch the current user's own draft content at a path (any kind)

    Args:
        workspace (str):
        kind (GetOwnDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetOwnDraftResponse200]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    kind: GetOwnDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetOwnDraftResponse200]]:
    """fetch the current user's own draft content at a path (any kind)

    Args:
        workspace (str):
        kind (GetOwnDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetOwnDraftResponse200]
    """

    return sync_detailed(
        workspace=workspace,
        kind=kind,
        path=path,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    kind: GetOwnDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[GetOwnDraftResponse200]]:
    """fetch the current user's own draft content at a path (any kind)

    Args:
        workspace (str):
        kind (GetOwnDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetOwnDraftResponse200]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    kind: GetOwnDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetOwnDraftResponse200]]:
    """fetch the current user's own draft content at a path (any kind)

    Args:
        workspace (str):
        kind (GetOwnDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetOwnDraftResponse200]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            kind=kind,
            path=path,
            client=client,
        )
    ).parsed
