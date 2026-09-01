from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_workspace_api_key_response_409 import (
    DeleteWorkspaceApiKeyResponse409,
)
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.workspace_api_key_response import WorkspaceApiKeyResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    api_key_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/workspaces/{workspace_id}/api-keys/{api_key_id}".format(
            workspace_id=quote(str(workspace_id), safe=""),
            api_key_id=quote(str(api_key_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DeleteWorkspaceApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceApiKeyResponse
    | None
):
    if response.status_code == 200:
        response_200 = WorkspaceApiKeyResponse.from_dict(response.json())

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
        response_409 = DeleteWorkspaceApiKeyResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    DeleteWorkspaceApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceApiKeyResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    api_key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    DeleteWorkspaceApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceApiKeyResponse
]:
    """RevokeWorkspaceApiKey


    Deletes an API key granted to the workspace. It stops working immediately.

    Requires MANAGE_WORKSPACE permission on the workspace.

    Args:
        workspace_id (UUID):
        api_key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteWorkspaceApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceApiKeyResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        api_key_id=api_key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    api_key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> (
    DeleteWorkspaceApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceApiKeyResponse
    | None
):
    """RevokeWorkspaceApiKey


    Deletes an API key granted to the workspace. It stops working immediately.

    Requires MANAGE_WORKSPACE permission on the workspace.

    Args:
        workspace_id (UUID):
        api_key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteWorkspaceApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceApiKeyResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        api_key_id=api_key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    api_key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[
    DeleteWorkspaceApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceApiKeyResponse
]:
    """RevokeWorkspaceApiKey


    Deletes an API key granted to the workspace. It stops working immediately.

    Requires MANAGE_WORKSPACE permission on the workspace.

    Args:
        workspace_id (UUID):
        api_key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteWorkspaceApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceApiKeyResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        api_key_id=api_key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    api_key_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> (
    DeleteWorkspaceApiKeyResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | WorkspaceApiKeyResponse
    | None
):
    """RevokeWorkspaceApiKey


    Deletes an API key granted to the workspace. It stops working immediately.

    Requires MANAGE_WORKSPACE permission on the workspace.

    Args:
        workspace_id (UUID):
        api_key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteWorkspaceApiKeyResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | WorkspaceApiKeyResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            api_key_id=api_key_id,
            client=client,
        )
    ).parsed
