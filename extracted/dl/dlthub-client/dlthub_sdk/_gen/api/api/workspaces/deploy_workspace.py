from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deploy_workspace_request import DeployWorkspaceRequest
from ...models.deploy_workspace_response import DeployWorkspaceResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    *,
    body: DeployWorkspaceRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/-deploy".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeployWorkspaceResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = DeployWorkspaceResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DeployWorkspaceResponse | ErrorResponse]:
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
    body: DeployWorkspaceRequest,
) -> Response[DeployWorkspaceResponse | ErrorResponse]:
    """Deploy

    Deploys a set of job definitions from a deployment manifest. Creates new jobs,
    updates existing ones, and archives orphaned jobs (those previously deployed from
    the same deployment_module but no longer present in the manifest).

    Answers with one receipt per kind the manifest declares. Under `jobs`, `succeeded` lists each
    job created, updated or archived with its `outcome` and `skipped` the unchanged ones; a deploy
    is all or nothing, so `failed` is empty.

    When deployment_module is None, this is an ad-hoc deploy: jobs are only added or
    updated, never archived. When deployment_module is '__deployment__', the workspace
    description is also updated from the manifest.

    Supports dry_run mode to preview changes without persisting.

    Requires WRITE permission on the workspace level.

    Args:
        workspace_id (UUID):
        body (DeployWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeployWorkspaceResponse | ErrorResponse]
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
    body: DeployWorkspaceRequest,
) -> DeployWorkspaceResponse | ErrorResponse | None:
    """Deploy

    Deploys a set of job definitions from a deployment manifest. Creates new jobs,
    updates existing ones, and archives orphaned jobs (those previously deployed from
    the same deployment_module but no longer present in the manifest).

    Answers with one receipt per kind the manifest declares. Under `jobs`, `succeeded` lists each
    job created, updated or archived with its `outcome` and `skipped` the unchanged ones; a deploy
    is all or nothing, so `failed` is empty.

    When deployment_module is None, this is an ad-hoc deploy: jobs are only added or
    updated, never archived. When deployment_module is '__deployment__', the workspace
    description is also updated from the manifest.

    Supports dry_run mode to preview changes without persisting.

    Requires WRITE permission on the workspace level.

    Args:
        workspace_id (UUID):
        body (DeployWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeployWorkspaceResponse | ErrorResponse
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
    body: DeployWorkspaceRequest,
) -> Response[DeployWorkspaceResponse | ErrorResponse]:
    """Deploy

    Deploys a set of job definitions from a deployment manifest. Creates new jobs,
    updates existing ones, and archives orphaned jobs (those previously deployed from
    the same deployment_module but no longer present in the manifest).

    Answers with one receipt per kind the manifest declares. Under `jobs`, `succeeded` lists each
    job created, updated or archived with its `outcome` and `skipped` the unchanged ones; a deploy
    is all or nothing, so `failed` is empty.

    When deployment_module is None, this is an ad-hoc deploy: jobs are only added or
    updated, never archived. When deployment_module is '__deployment__', the workspace
    description is also updated from the manifest.

    Supports dry_run mode to preview changes without persisting.

    Requires WRITE permission on the workspace level.

    Args:
        workspace_id (UUID):
        body (DeployWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeployWorkspaceResponse | ErrorResponse]
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
    body: DeployWorkspaceRequest,
) -> DeployWorkspaceResponse | ErrorResponse | None:
    """Deploy

    Deploys a set of job definitions from a deployment manifest. Creates new jobs,
    updates existing ones, and archives orphaned jobs (those previously deployed from
    the same deployment_module but no longer present in the manifest).

    Answers with one receipt per kind the manifest declares. Under `jobs`, `succeeded` lists each
    job created, updated or archived with its `outcome` and `skipped` the unchanged ones; a deploy
    is all or nothing, so `failed` is empty.

    When deployment_module is None, this is an ad-hoc deploy: jobs are only added or
    updated, never archived. When deployment_module is '__deployment__', the workspace
    description is also updated from the manifest.

    Supports dry_run mode to preview changes without persisting.

    Requires WRITE permission on the workspace level.

    Args:
        workspace_id (UUID):
        body (DeployWorkspaceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeployWorkspaceResponse | ErrorResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
