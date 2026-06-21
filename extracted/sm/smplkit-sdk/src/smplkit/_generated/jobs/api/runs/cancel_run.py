from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.run_response import RunResponse
from uuid import UUID


def _get_kwargs(
    run_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/runs/{run_id}/actions/cancel".format(
            run_id=quote(str(run_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | RunResponse | None:
    if response.status_code == 200:
        response_200 = RunResponse.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | RunResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | RunResponse]:
    r"""Cancel Run

     Cancel a pending or running run.

    Returns `404` if the run does not exist and `409` if it is already in a
    terminal state. Canceling a running run stops us tracking it, but the HTTP
    request may already be in flight — cancel means \"stop tracking,\" not
    \"guaranteed it didn't happen.\" A run that has already started running still
    counts toward your monthly run allowance even if you cancel it; a run
    canceled while it is still pending does not count.

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RunResponse]
    """

    kwargs = _get_kwargs(
        run_id=run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    run_id: UUID,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | RunResponse | None:
    r"""Cancel Run

     Cancel a pending or running run.

    Returns `404` if the run does not exist and `409` if it is already in a
    terminal state. Canceling a running run stops us tracking it, but the HTTP
    request may already be in flight — cancel means \"stop tracking,\" not
    \"guaranteed it didn't happen.\" A run that has already started running still
    counts toward your monthly run allowance even if you cancel it; a run
    canceled while it is still pending does not count.

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RunResponse
    """

    return sync_detailed(
        run_id=run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    run_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | RunResponse]:
    r"""Cancel Run

     Cancel a pending or running run.

    Returns `404` if the run does not exist and `409` if it is already in a
    terminal state. Canceling a running run stops us tracking it, but the HTTP
    request may already be in flight — cancel means \"stop tracking,\" not
    \"guaranteed it didn't happen.\" A run that has already started running still
    counts toward your monthly run allowance even if you cancel it; a run
    canceled while it is still pending does not count.

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RunResponse]
    """

    kwargs = _get_kwargs(
        run_id=run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    run_id: UUID,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | RunResponse | None:
    r"""Cancel Run

     Cancel a pending or running run.

    Returns `404` if the run does not exist and `409` if it is already in a
    terminal state. Canceling a running run stops us tracking it, but the HTTP
    request may already be in flight — cancel means \"stop tracking,\" not
    \"guaranteed it didn't happen.\" A run that has already started running still
    counts toward your monthly run allowance even if you cancel it; a run
    canceled while it is still pending does not count.

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RunResponse
    """

    return (
        await asyncio_detailed(
            run_id=run_id,
            client=client,
        )
    ).parsed
