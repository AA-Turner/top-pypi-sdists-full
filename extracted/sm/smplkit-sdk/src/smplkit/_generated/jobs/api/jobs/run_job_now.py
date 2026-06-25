from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.run_now_request import RunNowRequest
from ...models.run_response import RunResponse
from ...types import Unset


def _get_kwargs(
    job_id: str,
    *,
    body: None | RunNowRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/jobs/{job_id}/actions/run".format(
            job_id=quote(str(job_id), safe=""),
        ),
    }

    if isinstance(body, RunNowRequest):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
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
    body: None | RunNowRequest | Unset = UNSET,
) -> Response[RunResponse]:
    r"""Run Job Now

     Trigger one immediate run of the job in a specified environment (a
    `MANUAL` run).

    This is the primary execution path for a manual job and is also usable ad
    hoc for a recurring job (\"run now\"). The job's schedule and enabled state are
    untouched. The run executes in the environment named by the request body's
    `environment`; when the job is enabled in exactly one environment that
    environment is used, and a single-environment credential implies it. The
    environment must be one the job is **enabled** in (409 otherwise). The run
    executes the job's effective configuration for that environment. It is
    enqueued and executed by the worker; if the account is over its run
    allotment the run will fail with reason `QUOTA_EXCEEDED` rather than being
    rejected here.

    Args:
        job_id (str):
        body (None | RunNowRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunResponse]
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
    body: None | RunNowRequest | Unset = UNSET,
) -> RunResponse | None:
    r"""Run Job Now

     Trigger one immediate run of the job in a specified environment (a
    `MANUAL` run).

    This is the primary execution path for a manual job and is also usable ad
    hoc for a recurring job (\"run now\"). The job's schedule and enabled state are
    untouched. The run executes in the environment named by the request body's
    `environment`; when the job is enabled in exactly one environment that
    environment is used, and a single-environment credential implies it. The
    environment must be one the job is **enabled** in (409 otherwise). The run
    executes the job's effective configuration for that environment. It is
    enqueued and executed by the worker; if the account is over its run
    allotment the run will fail with reason `QUOTA_EXCEEDED` rather than being
    rejected here.

    Args:
        job_id (str):
        body (None | RunNowRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunResponse
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
    body: None | RunNowRequest | Unset = UNSET,
) -> Response[RunResponse]:
    r"""Run Job Now

     Trigger one immediate run of the job in a specified environment (a
    `MANUAL` run).

    This is the primary execution path for a manual job and is also usable ad
    hoc for a recurring job (\"run now\"). The job's schedule and enabled state are
    untouched. The run executes in the environment named by the request body's
    `environment`; when the job is enabled in exactly one environment that
    environment is used, and a single-environment credential implies it. The
    environment must be one the job is **enabled** in (409 otherwise). The run
    executes the job's effective configuration for that environment. It is
    enqueued and executed by the worker; if the account is over its run
    allotment the run will fail with reason `QUOTA_EXCEEDED` rather than being
    rejected here.

    Args:
        job_id (str):
        body (None | RunNowRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunResponse]
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
    body: None | RunNowRequest | Unset = UNSET,
) -> RunResponse | None:
    r"""Run Job Now

     Trigger one immediate run of the job in a specified environment (a
    `MANUAL` run).

    This is the primary execution path for a manual job and is also usable ad
    hoc for a recurring job (\"run now\"). The job's schedule and enabled state are
    untouched. The run executes in the environment named by the request body's
    `environment`; when the job is enabled in exactly one environment that
    environment is used, and a single-environment credential implies it. The
    environment must be one the job is **enabled** in (409 otherwise). The run
    executes the job's effective configuration for that environment. It is
    enqueued and executed by the worker; if the account is over its run
    allotment the run will fail with reason `QUOTA_EXCEEDED` rather than being
    rejected here.

    Args:
        job_id (str):
        body (None | RunNowRequest | Unset):

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
            body=body,
        )
    ).parsed
