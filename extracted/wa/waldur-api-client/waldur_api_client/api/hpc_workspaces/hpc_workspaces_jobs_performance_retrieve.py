from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hpc_job_performance import HpcJobPerformance
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    job_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/hpc-workspaces/{uuid}/jobs/{job_id}/performance/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> HpcJobPerformance:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = HpcJobPerformance.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HpcJobPerformance]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HpcJobPerformance]:
    """Get the performance of a job over its run

     Per-GPU use, GPU memory and power, CPU cores and host memory over the job's run, and its busiest
    processes, from the cluster monitor (slurm-monitor with Sonar probes) as the signed-in user.

    Args:
        uuid (UUID):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcJobPerformance]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> HpcJobPerformance:
    """Get the performance of a job over its run

     Per-GPU use, GPU memory and power, CPU cores and host memory over the job's run, and its busiest
    processes, from the cluster monitor (slurm-monitor with Sonar probes) as the signed-in user.

    Args:
        uuid (UUID):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcJobPerformance
    """

    return sync_detailed(
        uuid=uuid,
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HpcJobPerformance]:
    """Get the performance of a job over its run

     Per-GPU use, GPU memory and power, CPU cores and host memory over the job's run, and its busiest
    processes, from the cluster monitor (slurm-monitor with Sonar probes) as the signed-in user.

    Args:
        uuid (UUID):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcJobPerformance]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> HpcJobPerformance:
    """Get the performance of a job over its run

     Per-GPU use, GPU memory and power, CPU cores and host memory over the job's run, and its busiest
    processes, from the cluster monitor (slurm-monitor with Sonar probes) as the signed-in user.

    Args:
        uuid (UUID):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcJobPerformance
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            job_id=job_id,
            client=client,
        )
    ).parsed
