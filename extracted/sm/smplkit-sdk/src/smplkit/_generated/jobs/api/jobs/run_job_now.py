from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.run_response import RunResponse
from ...types import Unset


def _get_kwargs(
    job_id: str,
    *,
    x_smplkit_environment: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_smplkit_environment, Unset):
        headers["X-Smplkit-Environment"] = x_smplkit_environment

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/jobs/{job_id}/actions/run".format(
            job_id=quote(str(job_id), safe=""),
        ),
    }

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
    x_smplkit_environment: None | str | Unset = UNSET,
) -> Response[RunResponse]:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run executes in the
    environment named by the `X-Smplkit-Environment` header; when the job is
    enabled in exactly one environment that environment is used, and a
    single-environment credential implies it. The run executes the job's
    effective configuration for that environment. It is enqueued and executed
    by the worker; if the account is over its run allotment the run will fail
    with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
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
    x_smplkit_environment: None | str | Unset = UNSET,
) -> RunResponse | None:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run executes in the
    environment named by the `X-Smplkit-Environment` header; when the job is
    enabled in exactly one environment that environment is used, and a
    single-environment credential implies it. The run executes the job's
    effective configuration for that environment. It is enqueued and executed
    by the worker; if the account is over its run allotment the run will fail
    with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RunResponse
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        x_smplkit_environment=x_smplkit_environment,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,
    x_smplkit_environment: None | str | Unset = UNSET,
) -> Response[RunResponse]:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run executes in the
    environment named by the `X-Smplkit-Environment` header; when the job is
    enabled in exactly one environment that environment is used, and a
    single-environment credential implies it. The run executes the job's
    effective configuration for that environment. It is enqueued and executed
    by the worker; if the account is over its run allotment the run will fail
    with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RunResponse]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        x_smplkit_environment=x_smplkit_environment,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: AuthenticatedClient,
    x_smplkit_environment: None | str | Unset = UNSET,
) -> RunResponse | None:
    """Run Job Now

     Trigger one immediate run of the job (a `MANUAL` run).

    The job's schedule and enabled state are untouched. The run executes in the
    environment named by the `X-Smplkit-Environment` header; when the job is
    enabled in exactly one environment that environment is used, and a
    single-environment credential implies it. The run executes the job's
    effective configuration for that environment. It is enqueued and executed
    by the worker; if the account is over its run allotment the run will fail
    with reason `QUOTA_EXCEEDED` rather than being rejected here.

    Args:
        job_id (str):
        x_smplkit_environment (None | str | Unset): The environment to operate in. Names the
            single environment a one-off job is born in (or a manual run executes in). Optional when
            the credential is scoped to a single environment (which is then implied); required when
            the credential can reach several environments and the choice is otherwise ambiguous.
            Ignored for a recurring job, whose environments come from its `environments` map.

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
            x_smplkit_environment=x_smplkit_environment,
        )
    ).parsed
