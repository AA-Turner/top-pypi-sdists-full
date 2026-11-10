from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hpc_job_output import HpcJobOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    job_id: str,
    *,
    lines: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["lines"] = lines

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/hpc-workspaces/{uuid}/jobs/{job_id}/output/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> HpcJobOutput:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = HpcJobOutput.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[HpcJobOutput]:
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
    lines: Union[Unset, int] = 100,
) -> Response[HpcJobOutput]:
    """Get the script and output of a job

     The batch script and the last lines of standard output and error.

    Args:
        uuid (UUID):
        job_id (str):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcJobOutput]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        job_id=job_id,
        lines=lines,
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
    lines: Union[Unset, int] = 100,
) -> HpcJobOutput:
    """Get the script and output of a job

     The batch script and the last lines of standard output and error.

    Args:
        uuid (UUID):
        job_id (str):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcJobOutput
    """

    return sync_detailed(
        uuid=uuid,
        job_id=job_id,
        client=client,
        lines=lines,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    job_id: str,
    *,
    client: AuthenticatedClient,
    lines: Union[Unset, int] = 100,
) -> Response[HpcJobOutput]:
    """Get the script and output of a job

     The batch script and the last lines of standard output and error.

    Args:
        uuid (UUID):
        job_id (str):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcJobOutput]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        job_id=job_id,
        lines=lines,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    job_id: str,
    *,
    client: AuthenticatedClient,
    lines: Union[Unset, int] = 100,
) -> HpcJobOutput:
    """Get the script and output of a job

     The batch script and the last lines of standard output and error.

    Args:
        uuid (UUID):
        job_id (str):
        lines (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcJobOutput
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            job_id=job_id,
            client=client,
            lines=lines,
        )
    ).parsed
