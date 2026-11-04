from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.issue_upload_deployment_response import IssueUploadDeploymentResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/deployments/-issue-upload".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | IssueUploadDeploymentResponse | None:
    if response.status_code == 200:
        response_200 = IssueUploadDeploymentResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | IssueUploadDeploymentResponse]:
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
) -> Response[ErrorResponse | IssueUploadDeploymentResponse]:
    """IssueUploadDeployment

    Prepares the upload of a new deployment. Send a multipart POST with `file` (the package) and
    `requirements_file` to
    `upload_url`, with `Authorization: Bearer <upload_token>`, within 10 minutes. The deployment
    exists, under `deployment_id`, only after the upload succeeds.

    Requires the developer role (or higher) in the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IssueUploadDeploymentResponse]
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
) -> ErrorResponse | IssueUploadDeploymentResponse | None:
    """IssueUploadDeployment

    Prepares the upload of a new deployment. Send a multipart POST with `file` (the package) and
    `requirements_file` to
    `upload_url`, with `Authorization: Bearer <upload_token>`, within 10 minutes. The deployment
    exists, under `deployment_id`, only after the upload succeeds.

    Requires the developer role (or higher) in the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IssueUploadDeploymentResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | IssueUploadDeploymentResponse]:
    """IssueUploadDeployment

    Prepares the upload of a new deployment. Send a multipart POST with `file` (the package) and
    `requirements_file` to
    `upload_url`, with `Authorization: Bearer <upload_token>`, within 10 minutes. The deployment
    exists, under `deployment_id`, only after the upload succeeds.

    Requires the developer role (or higher) in the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | IssueUploadDeploymentResponse]
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
) -> ErrorResponse | IssueUploadDeploymentResponse | None:
    """IssueUploadDeployment

    Prepares the upload of a new deployment. Send a multipart POST with `file` (the package) and
    `requirements_file` to
    `upload_url`, with `Authorization: Bearer <upload_token>`, within 10 minutes. The deployment
    exists, under `deployment_id`, only after the upload succeeds.

    Requires the developer role (or higher) in the workspace.

    Args:
        workspace_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | IssueUploadDeploymentResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
        )
    ).parsed
