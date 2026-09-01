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
from ...models.update_workspace_member_request import UpdateWorkspaceMemberRequest
from ...models.update_workspace_member_response_409 import (
    UpdateWorkspaceMemberResponse409,
)
from ...models.workspace_member_response import WorkspaceMemberResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    user_id: str,
    *,
    body: UpdateWorkspaceMemberRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/workspaces/{workspace_id}/members/{user_id}".format(
            workspace_id=quote(str(workspace_id), safe=""),
            user_id=quote(str(user_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UpdateWorkspaceMemberResponse409
    | WorkspaceMemberResponse
    | None
):
    if response.status_code == 200:
        response_200 = WorkspaceMemberResponse.from_dict(response.json())

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
        response_409 = UpdateWorkspaceMemberResponse409.from_dict(response.json())

        return response_409

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
    | UpdateWorkspaceMemberResponse409
    | WorkspaceMemberResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceMemberRequest,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UpdateWorkspaceMemberResponse409
    | WorkspaceMemberResponse
]:
    """UpdateWorkspaceMember


    Changes a member's role in a workspace (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_WORKSPACE permission on the workspace level.

    Args:
        workspace_id (UUID):
        user_id (str):
        body (UpdateWorkspaceMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UpdateWorkspaceMemberResponse409 | WorkspaceMemberResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceMemberRequest,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UpdateWorkspaceMemberResponse409
    | WorkspaceMemberResponse
    | None
):
    """UpdateWorkspaceMember


    Changes a member's role in a workspace (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_WORKSPACE permission on the workspace level.

    Args:
        workspace_id (UUID):
        user_id (str):
        body (UpdateWorkspaceMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UpdateWorkspaceMemberResponse409 | WorkspaceMemberResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceMemberRequest,
) -> Response[
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UpdateWorkspaceMemberResponse409
    | WorkspaceMemberResponse
]:
    """UpdateWorkspaceMember


    Changes a member's role in a workspace (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_WORKSPACE permission on the workspace level.

    Args:
        workspace_id (UUID):
        user_id (str):
        body (UpdateWorkspaceMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UpdateWorkspaceMemberResponse409 | WorkspaceMemberResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    user_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateWorkspaceMemberRequest,
) -> (
    ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | UpdateWorkspaceMemberResponse409
    | WorkspaceMemberResponse
    | None
):
    """UpdateWorkspaceMember


    Changes a member's role in a workspace (including promotion to owner).

    You cannot change your own membership. The last owner cannot be demoted.

    Requires MANAGE_WORKSPACE permission on the workspace level.

    Args:
        workspace_id (UUID):
        user_id (str):
        body (UpdateWorkspaceMemberRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | UpdateWorkspaceMemberResponse409 | WorkspaceMemberResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
