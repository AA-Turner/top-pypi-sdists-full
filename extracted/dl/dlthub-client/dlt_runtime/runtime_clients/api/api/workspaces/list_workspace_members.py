from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.principal_kind import PrincipalKind
from ...models.workspace_member_response import WorkspaceMemberResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_id: UUID,
    *,
    kind: list[PrincipalKind] | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_kind: list[str] | None | Unset
    if isinstance(kind, Unset):
        json_kind = UNSET
    elif isinstance(kind, list):
        json_kind = []
        for kind_type_0_item_data in kind:
            kind_type_0_item = kind_type_0_item_data.value
            json_kind.append(kind_type_0_item)

    else:
        json_kind = kind
    params["kind"] = json_kind

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/workspaces/{workspace_id}/members".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[WorkspaceMemberResponse]
    | None
):
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkspaceMemberResponse.from_dict(
                response_200_item_data
            )

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[WorkspaceMemberResponse]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    kind: list[PrincipalKind] | None | Unset = UNSET,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[WorkspaceMemberResponse]
]:
    """ListWorkspaceMembers

     List a workspace's members. Returns all members by default; pass one or more `kind` values to
    filter. Requires READ permission on the workspace.

    Args:
        workspace_id (UUID):
        kind (list[PrincipalKind] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[WorkspaceMemberResponse]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        kind=kind,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    kind: list[PrincipalKind] | None | Unset = UNSET,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[WorkspaceMemberResponse]
    | None
):
    """ListWorkspaceMembers

     List a workspace's members. Returns all members by default; pass one or more `kind` values to
    filter. Requires READ permission on the workspace.

    Args:
        workspace_id (UUID):
        kind (list[PrincipalKind] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[WorkspaceMemberResponse]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        kind=kind,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    kind: list[PrincipalKind] | None | Unset = UNSET,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[WorkspaceMemberResponse]
]:
    """ListWorkspaceMembers

     List a workspace's members. Returns all members by default; pass one or more `kind` values to
    filter. Requires READ permission on the workspace.

    Args:
        workspace_id (UUID):
        kind (list[PrincipalKind] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[WorkspaceMemberResponse]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        kind=kind,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    kind: list[PrincipalKind] | None | Unset = UNSET,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | list[WorkspaceMemberResponse]
    | None
):
    """ListWorkspaceMembers

     List a workspace's members. Returns all members by default; pass one or more `kind` values to
    filter. Requires READ permission on the workspace.

    Args:
        workspace_id (UUID):
        kind (list[PrincipalKind] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | list[WorkspaceMemberResponse]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            kind=kind,
        )
    ).parsed
