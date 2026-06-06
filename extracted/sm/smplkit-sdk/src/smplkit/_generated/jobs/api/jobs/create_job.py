from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.job_create_request import JobCreateRequest
from ...models.job_response import JobResponse


def _get_kwargs(
    *,
    body: JobCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/jobs",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> JobResponse | None:
    if response.status_code == 201:
        response_201 = JobResponse.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[JobResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: JobCreateRequest,
) -> Response[JobResponse]:
    """Create Job

     Create a job for this account.

    The caller supplies the job's id as `data.id`. Ids are unique
    within an account and immutable. An enabled job begins scheduling
    immediately.

    Args:
        body (JobCreateRequest): JSON:API request envelope for creating a job (caller-supplied
            `data.id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: JobCreateRequest,
) -> JobResponse | None:
    """Create Job

     Create a job for this account.

    The caller supplies the job's id as `data.id`. Ids are unique
    within an account and immutable. An enabled job begins scheduling
    immediately.

    Args:
        body (JobCreateRequest): JSON:API request envelope for creating a job (caller-supplied
            `data.id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: JobCreateRequest,
) -> Response[JobResponse]:
    """Create Job

     Create a job for this account.

    The caller supplies the job's id as `data.id`. Ids are unique
    within an account and immutable. An enabled job begins scheduling
    immediately.

    Args:
        body (JobCreateRequest): JSON:API request envelope for creating a job (caller-supplied
            `data.id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: JobCreateRequest,
) -> JobResponse | None:
    """Create Job

     Create a job for this account.

    The caller supplies the job's id as `data.id`. Ids are unique
    within an account and immutable. An enabled job begins scheduling
    immediately.

    Args:
        body (JobCreateRequest): JSON:API request envelope for creating a job (caller-supplied
            `data.id`).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
