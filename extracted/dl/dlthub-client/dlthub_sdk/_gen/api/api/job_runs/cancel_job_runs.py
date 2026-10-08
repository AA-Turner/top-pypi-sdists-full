from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cancel_job_runs_request import CancelJobRunsRequest
from ...models.cancel_job_runs_response import CancelJobRunsResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    *,
    body: CancelJobRunsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/job-runs/-cancel".format(
            workspace_id=quote(str(workspace_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CancelJobRunsResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CancelJobRunsResponse.from_dict(response.json())

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
) -> Response[CancelJobRunsResponse | ErrorResponse]:
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
    body: CancelJobRunsRequest,
) -> Response[CancelJobRunsResponse | ErrorResponse]:
    """CancelJobRuns

    Cancel the given runs in a single transaction.

    Answers a receipt: `succeeded` runs were cancelled, `skipped` runs were already in a terminal
    state, `failed` lists ids that name no run in the workspace. Use `dry_run=true` to preview
    without cancelling.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CancelJobRunsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelJobRunsResponse | ErrorResponse]
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
    body: CancelJobRunsRequest,
) -> CancelJobRunsResponse | ErrorResponse | None:
    """CancelJobRuns

    Cancel the given runs in a single transaction.

    Answers a receipt: `succeeded` runs were cancelled, `skipped` runs were already in a terminal
    state, `failed` lists ids that name no run in the workspace. Use `dry_run=true` to preview
    without cancelling.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CancelJobRunsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelJobRunsResponse | ErrorResponse
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
    body: CancelJobRunsRequest,
) -> Response[CancelJobRunsResponse | ErrorResponse]:
    """CancelJobRuns

    Cancel the given runs in a single transaction.

    Answers a receipt: `succeeded` runs were cancelled, `skipped` runs were already in a terminal
    state, `failed` lists ids that name no run in the workspace. Use `dry_run=true` to preview
    without cancelling.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CancelJobRunsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CancelJobRunsResponse | ErrorResponse]
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
    body: CancelJobRunsRequest,
) -> CancelJobRunsResponse | ErrorResponse | None:
    """CancelJobRuns

    Cancel the given runs in a single transaction.

    Answers a receipt: `succeeded` runs were cancelled, `skipped` runs were already in a terminal
    state, `failed` lists ids that name no run in the workspace. Use `dry_run=true` to preview
    without cancelling.

    Requires WRITE permission on the workspace.

    Args:
        workspace_id (UUID):
        body (CancelJobRunsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CancelJobRunsResponse | ErrorResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            client=client,
            body=body,
        )
    ).parsed
