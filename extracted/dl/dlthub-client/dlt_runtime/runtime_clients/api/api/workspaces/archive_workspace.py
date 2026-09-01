from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.archive_workspace_response_409 import ArchiveWorkspaceResponse409
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.workspace_response import WorkspaceResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/workspaces/{workspace_id}/archive".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ArchiveWorkspaceResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceResponse
    | None
):
    if response.status_code == 200:
        response_200 = WorkspaceResponse.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = ArchiveWorkspaceResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    ArchiveWorkspaceResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceResponse
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
) -> Response[
    ArchiveWorkspaceResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceResponse
]:
    """ArchiveWorkspace


    Archives a workspace: clears schedules and rejects further mutations until unarchived.
    Refuses with 409 if any run is still active, and with 400 for playground workspaces.

    Requires MANAGE_WORKSPACE permission.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArchiveWorkspaceResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> (
    ArchiveWorkspaceResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceResponse
    | None
):
    """ArchiveWorkspace


    Archives a workspace: clears schedules and rejects further mutations until unarchived.
    Refuses with 409 if any run is still active, and with 400 for playground workspaces.

    Requires MANAGE_WORKSPACE permission.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArchiveWorkspaceResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    ArchiveWorkspaceResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceResponse
]:
    """ArchiveWorkspace


    Archives a workspace: clears schedules and rejects further mutations until unarchived.
    Refuses with 409 if any run is still active, and with 400 for playground workspaces.

    Requires MANAGE_WORKSPACE permission.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArchiveWorkspaceResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> (
    ArchiveWorkspaceResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceResponse
    | None
):
    """ArchiveWorkspace


    Archives a workspace: clears schedules and rejects further mutations until unarchived.
    Refuses with 409 if any run is still active, and with 400 for playground workspaces.

    Requires MANAGE_WORKSPACE permission.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArchiveWorkspaceResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
