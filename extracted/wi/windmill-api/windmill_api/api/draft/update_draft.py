from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_draft_json_body import UpdateDraftJsonBody
from ...models.update_draft_kind import UpdateDraftKind
from ...models.update_draft_response_200 import UpdateDraftResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    kind: UpdateDraftKind,
    path: str,
    *,
    json_body: UpdateDraftJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/drafts/update/{kind}/{path}".format(
            workspace=workspace,
            kind=kind,
            path=path,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateDraftResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateDraftResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateDraftResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    kind: UpdateDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateDraftJsonBody,
) -> Response[UpdateDraftResponse200]:
    """upsert (or clear) the current user's draft at a path

    Args:
        workspace (str):
        kind (UpdateDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        json_body (UpdateDraftJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateDraftResponse200]
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


def sync(
    workspace: str,
    kind: UpdateDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateDraftJsonBody,
) -> Optional[UpdateDraftResponse200]:
    """upsert (or clear) the current user's draft at a path

    Args:
        workspace (str):
        kind (UpdateDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        json_body (UpdateDraftJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateDraftResponse200
    """

    return sync_detailed(
        workspace=workspace,
        kind=kind,
        path=path,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    kind: UpdateDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateDraftJsonBody,
) -> Response[UpdateDraftResponse200]:
    """upsert (or clear) the current user's draft at a path

    Args:
        workspace (str):
        kind (UpdateDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        json_body (UpdateDraftJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateDraftResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    kind: UpdateDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateDraftJsonBody,
) -> Optional[UpdateDraftResponse200]:
    """upsert (or clear) the current user's draft at a path

    Args:
        workspace (str):
        kind (UpdateDraftKind): Closed set of item kinds a user can autosave as a draft. Mirrors
            the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
        json_body (UpdateDraftJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateDraftResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            kind=kind,
            path=path,
            client=client,
            json_body=json_body,
        )
    ).parsed
