from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_draft_for_user_kind import DeleteDraftForUserKind
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    kind: DeleteDraftForUserKind,
    path: str,
    *,
    username: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": "/w/{workspace}/drafts/delete_for_user/{kind}/{path}".format(
            workspace=workspace,
            kind=kind,
            path=path,
        ),
        "params": params,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    kind: DeleteDraftForUserKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    username: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """delete another user's draft, or every draft at a path (admin only)

     Delete the draft a given user holds at a path, or, without `username`, every draft at that path (the
    legacy ownerless one and the caller's own included). Workspace admins / superadmins only, and only
    for script, flow, app and raw_app drafts. Unlike a discard of one's own draft through
    `drafts/update`, this returns 404 when nothing was deleted.

    Args:
        workspace (str):
        kind (DeleteDraftForUserKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    workspace: str,
    kind: DeleteDraftForUserKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    username: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """delete another user's draft, or every draft at a path (admin only)

     Delete the draft a given user holds at a path, or, without `username`, every draft at that path (the
    legacy ownerless one and the caller's own included). Workspace admins / superadmins only, and only
    for script, flow, app and raw_app drafts. Unlike a discard of one's own draft through
    `drafts/update`, this returns 404 when nothing was deleted.

    Args:
        workspace (str):
        kind (DeleteDraftForUserKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        username (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
