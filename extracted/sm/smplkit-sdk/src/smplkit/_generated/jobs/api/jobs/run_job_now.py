from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.run_response import RunResponse


def _get_kwargs(
    job_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/jobs/{job_id}/actions/run".format(
            job_id=quote(str(job_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> RunResponse | None:
    if response.status_code == 200:
        response_200 = RunResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[RunResponse]:
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
) -> Response[RunResponse]:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run is enqueued and
    executed by the worker; if the account is over its run allotment the run
    will fail with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> RunResponse | None:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run is enqueued and
    executed by the worker; if the account is over its run allotment the run
    will fail with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunResponse
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[RunResponse]:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run is enqueued and
    executed by the worker; if the account is over its run allotment the run
    will fail with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> RunResponse | None:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run is enqueued and
    executed by the worker; if the account is over its run allotment the run
    will fail with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunResponse
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
        )
    ).parsed
