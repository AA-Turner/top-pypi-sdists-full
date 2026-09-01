from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_or_update_script_response_409 import (
    CreateOrUpdateScriptResponse409,
)
from ...models.create_script_request import CreateScriptRequest
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.script_response import ScriptResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    *,
    body: CreateScriptRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/scripts".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    CreateOrUpdateScriptResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
    | None
):
    if response.status_code == 201:
        response_201 = ScriptResponse.from_dict(response.json())

        return response_201

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
        response_409 = CreateOrUpdateScriptResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateOrUpdateScriptResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
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
    body: CreateScriptRequest,
) -> Response[
    CreateOrUpdateScriptResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
]:
    """CreateOrUpdateScript


    Creates or updates a script for a workspace. The script is keyed by ``job_ref`` within the
    workspace. Every write creates a new ScriptVersion (the highest version is the active one).
    Scripts define entry points for the currently active deployment and can be archived to
    prevent scheduled runs or public endpoint access.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        body (CreateScriptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateOrUpdateScriptResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateScriptRequest,
) -> (
    CreateOrUpdateScriptResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
    | None
):
    """CreateOrUpdateScript


    Creates or updates a script for a workspace. The script is keyed by ``job_ref`` within the
    workspace. Every write creates a new ScriptVersion (the highest version is the active one).
    Scripts define entry points for the currently active deployment and can be archived to
    prevent scheduled runs or public endpoint access.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        body (CreateScriptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateOrUpdateScriptResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse
    """

    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateScriptRequest,
) -> Response[
    CreateOrUpdateScriptResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
]:
    """CreateOrUpdateScript


    Creates or updates a script for a workspace. The script is keyed by ``job_ref`` within the
    workspace. Every write creates a new ScriptVersion (the highest version is the active one).
    Scripts define entry points for the currently active deployment and can be archived to
    prevent scheduled runs or public endpoint access.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        body (CreateScriptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateOrUpdateScriptResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CreateScriptRequest,
) -> (
    CreateOrUpdateScriptResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | ScriptResponse
    | None
):
    """CreateOrUpdateScript


    Creates or updates a script for a workspace. The script is keyed by ``job_ref`` within the
    workspace. Every write creates a new ScriptVersion (the highest version is the active one).
    Scripts define entry points for the currently active deployment and can be archived to
    prevent scheduled runs or public endpoint access.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        body (CreateScriptRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateOrUpdateScriptResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | ScriptResponse
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
