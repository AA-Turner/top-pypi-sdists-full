from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_draft_for_user_kind import GetDraftForUserKind
from ...models.get_draft_for_user_response_200 import GetDraftForUserResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    kind: GetDraftForUserKind,
    path: str,
    *,
    username: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/drafts/get/{kind}/{path}".format(
            workspace=workspace,
            kind=kind,
            path=path,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetDraftForUserResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDraftForUserResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, GetDraftForUserResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    kind: GetDraftForUserKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    username: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, GetDraftForUserResponse200]]:
    """fetch a single draft's content by workspace username (or the legacy workspace-level row)

    Args:
        workspace (str):
        kind (GetDraftForUserKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetDraftForUserResponse200]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    kind: GetDraftForUserKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    username: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, GetDraftForUserResponse200]]:
    """fetch a single draft's content by workspace username (or the legacy workspace-level row)

    Args:
        workspace (str):
        kind (GetDraftForUserKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetDraftForUserResponse200]
    """

    return sync_detailed(
        workspace=workspace,
        kind=kind,
        path=path,
        client=client,
        username=username,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    kind: GetDraftForUserKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    username: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, GetDraftForUserResponse200]]:
    """fetch a single draft's content by workspace username (or the legacy workspace-level row)

    Args:
        workspace (str):
        kind (GetDraftForUserKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetDraftForUserResponse200]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    kind: GetDraftForUserKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    username: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, GetDraftForUserResponse200]]:
    """fetch a single draft's content by workspace username (or the legacy workspace-level row)

    Args:
        workspace (str):
        kind (GetDraftForUserKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetDraftForUserResponse200]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            kind=kind,
            path=path,
            client=client,
            username=username,
        )
    ).parsed
