from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.migrate_legacy_draft_json_body import MigrateLegacyDraftJsonBody
from ...models.migrate_legacy_draft_kind import MigrateLegacyDraftKind
from ...types import Response


def _get_kwargs(
    workspace: str,
    kind: MigrateLegacyDraftKind,
    path: str,
    *,
    json_body: MigrateLegacyDraftJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/drafts/migrate_legacy/{kind}/{path}".format(
            workspace=workspace,
            kind=kind,
            path=path,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
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
    kind: MigrateLegacyDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MigrateLegacyDraftJsonBody,
) -> Response[Any]:
    """resolve a legacy (workspace-level) draft (admin only)

     Delete a legacy draft (email NULL) or assign it to the authed admin as a per-user draft. Workspace
    admins / superadmins only.

    Args:
        workspace (str):
        kind (MigrateLegacyDraftKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        json_body (MigrateLegacyDraftJsonBody):

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
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    kind: MigrateLegacyDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MigrateLegacyDraftJsonBody,
) -> Response[Any]:
    """resolve a legacy (workspace-level) draft (admin only)

     Delete a legacy draft (email NULL) or assign it to the authed admin as a per-user draft. Workspace
    admins / superadmins only.

    Args:
        workspace (str):
        kind (MigrateLegacyDraftKind): Closed set of item kinds a user can autosave as a draft.
            Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        json_body (MigrateLegacyDraftJsonBody):

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
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
