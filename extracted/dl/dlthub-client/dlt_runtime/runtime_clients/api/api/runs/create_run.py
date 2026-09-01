from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_run_request import CreateRunRequest
from ...models.create_run_response_409 import CreateRunResponse409
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.triggered_job import TriggeredJob
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    *,
    body: CreateRunRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/runs".format(
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
    CreateRunResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | TriggeredJob
    | None
):
    if response.status_code == 201:
        response_201 = TriggeredJob.from_dict(response.json())

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
        response_409 = CreateRunResponse409.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    CreateRunResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | TriggeredJob
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
    body: CreateRunRequest,
) -> Response[
    CreateRunResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | TriggeredJob
]:
    """CreateRun


    Triggers a new run for a script in a workspace. The latest script version will be used. The profile
    associated with the script version will be used, of which
    the latest profile_version will be used. You may specify a specific profile to use.

    The script is identified by ID or job_ref.

    The mode parameter controls run creation behavior:
    - 'always' (default): Always creates a new run
    - 'when_not_running': Returns an existing active run if one exists, otherwise creates a new one

    Requires CREATE_RUN permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CreateRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateRunResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | TriggeredJob]
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
    body: CreateRunRequest,
) -> (
    CreateRunResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | TriggeredJob
    | None
):
    """CreateRun


    Triggers a new run for a script in a workspace. The latest script version will be used. The profile
    associated with the script version will be used, of which
    the latest profile_version will be used. You may specify a specific profile to use.

    The script is identified by ID or job_ref.

    The mode parameter controls run creation behavior:
    - 'always' (default): Always creates a new run
    - 'when_not_running': Returns an existing active run if one exists, otherwise creates a new one

    Requires CREATE_RUN permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CreateRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateRunResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | TriggeredJob
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
    body: CreateRunRequest,
) -> Response[
    CreateRunResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | TriggeredJob
]:
    """CreateRun


    Triggers a new run for a script in a workspace. The latest script version will be used. The profile
    associated with the script version will be used, of which
    the latest profile_version will be used. You may specify a specific profile to use.

    The script is identified by ID or job_ref.

    The mode parameter controls run creation behavior:
    - 'always' (default): Always creates a new run
    - 'when_not_running': Returns an existing active run if one exists, otherwise creates a new one

    Requires CREATE_RUN permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CreateRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateRunResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | TriggeredJob]
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
    body: CreateRunRequest,
) -> (
    CreateRunResponse409
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | TriggeredJob
    | None
):
    """CreateRun


    Triggers a new run for a script in a workspace. The latest script version will be used. The profile
    associated with the script version will be used, of which
    the latest profile_version will be used. You may specify a specific profile to use.

    The script is identified by ID or job_ref.

    The mode parameter controls run creation behavior:
    - 'always' (default): Always creates a new run
    - 'when_not_running': Returns an existing active run if one exists, otherwise creates a new one

    Requires CREATE_RUN permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CreateRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateRunResponse409 | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404 | TriggeredJob
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
