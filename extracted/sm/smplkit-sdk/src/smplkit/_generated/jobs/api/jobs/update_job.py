from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.job_request import JobRequest
from ...models.job_response import JobResponse


def _get_kwargs(
    job_id: str,
    *,
    body: JobRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/jobs/{job_id}".format(
            job_id=quote(str(job_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> JobResponse | None:
    if response.status_code == 200:
        response_200 = JobResponse.from_dict(response.json())

        return response_200

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
    job_id: str,
    *,
    client: AuthenticatedClient,
    body: JobRequest,
) -> Response[JobResponse]:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Enabling a paused job is a `PUT` with `enabled: true`; pausing is
    `enabled: false`. Editing the schedule recomputes the next fire time.

    Args:
        job_id (str):
        body (JobRequest): JSON:API request envelope for updating a job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: AuthenticatedClient,
    body: JobRequest,
) -> JobResponse | None:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Enabling a paused job is a `PUT` with `enabled: true`; pausing is
    `enabled: false`. Editing the schedule recomputes the next fire time.

    Args:
        job_id (str):
        body (JobRequest): JSON:API request envelope for updating a job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobResponse
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,
    body: JobRequest,
) -> Response[JobResponse]:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Enabling a paused job is a `PUT` with `enabled: true`; pausing is
    `enabled: false`. Editing the schedule recomputes the next fire time.

    Args:
        job_id (str):
        body (JobRequest): JSON:API request envelope for updating a job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: AuthenticatedClient,
    body: JobRequest,
) -> JobResponse | None:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Enabling a paused job is a `PUT` with `enabled: true`; pausing is
    `enabled: false`. Editing the schedule recomputes the next fire time.

    Args:
        job_id (str):
        body (JobRequest): JSON:API request envelope for updating a job.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobResponse
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            body=body,
        )
    ).parsed
