from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.job_response import JobResponse
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    job_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/jobs/{job_id}/-unpublish".format(
            workspace_id=quote(str(workspace_id), safe=""),
            job_id=quote(str(job_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | JobResponse | None:
    if response.status_code == 200:
        response_200 = JobResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | JobResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    job_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | JobResponse]:
    """UnpublishJob

    Disables the public URL for a job by clearing the public_secret. After calling this
    endpoint, the job will no longer be accessible via its public URL.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        job_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | JobResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    job_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | JobResponse | None:
    """UnpublishJob

    Disables the public URL for a job by clearing the public_secret. After calling this
    endpoint, the job will no longer be accessible via its public URL.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        job_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | JobResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    job_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | JobResponse]:
    """UnpublishJob

    Disables the public URL for a job by clearing the public_secret. After calling this
    endpoint, the job will no longer be accessible via its public URL.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        job_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | JobResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    job_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | JobResponse | None:
    """UnpublishJob

    Disables the public URL for a job by clearing the public_secret. After calling this
    endpoint, the job will no longer be accessible via its public URL.

    Requires WRITE permission on the organization level.

    Args:
        workspace_id (UUID):
        job_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | JobResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            job_id=job_id,
            client=client,
        )
    ).parsed
