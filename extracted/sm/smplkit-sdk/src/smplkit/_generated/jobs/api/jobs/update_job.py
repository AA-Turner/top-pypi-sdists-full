from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.job_request import JobRequest
from ...models.job_response import JobResponse
from ...types import Unset


def _get_kwargs(
    job_id: str,
    *,
    body: JobRequest,
    x_smplkit_environment: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_smplkit_environment, Unset):
        headers["X-Smplkit-Environment"] = x_smplkit_environment

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
    x_smplkit_environment: None | str | Unset = UNSET,
) -> Response[JobResponse]:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Set enablement per environment via the `environments` map (a recurring
    job), or by recreating a one-off job in the desired environment. Editing
    the schedule recomputes the next fire time; changing only which
    environments are enabled preserves the existing cadence.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.
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
        x_smplkit_environment=x_smplkit_environment,
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
    x_smplkit_environment: None | str | Unset = UNSET,
) -> JobResponse | None:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Set enablement per environment via the `environments` map (a recurring
    job), or by recreating a one-off job in the desired environment. Editing
    the schedule recomputes the next fire time; changing only which
    environments are enabled preserves the existing cadence.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.
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
        x_smplkit_environment=x_smplkit_environment,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,
    body: JobRequest,
    x_smplkit_environment: None | str | Unset = UNSET,
) -> Response[JobResponse]:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Set enablement per environment via the `environments` map (a recurring
    job), or by recreating a one-off job in the desired environment. Editing
    the schedule recomputes the next fire time; changing only which
    environments are enabled preserves the existing cadence.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.
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
        x_smplkit_environment=x_smplkit_environment,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: AuthenticatedClient,
    body: JobRequest,
    x_smplkit_environment: None | str | Unset = UNSET,
) -> JobResponse | None:
    """Update Job

     Replace an existing job. Every writable field is overwritten.

    Set enablement per environment via the `environments` map (a recurring
    job), or by recreating a one-off job in the desired environment. Editing
    the schedule recomputes the next fire time; changing only which
    environments are enabled preserves the existing cadence.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.
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
            x_smplkit_environment=x_smplkit_environment,
        )
    ).parsed
