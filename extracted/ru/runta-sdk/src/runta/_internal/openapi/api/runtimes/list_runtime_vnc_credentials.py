from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.error_envelope import ErrorEnvelope
from ...models.list_vnc_credentials_response import ListVncCredentialsResponse
from ...types import Response


def _get_kwargs(
    runtime_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v2/runtimes/{runtime_id}/vnc-credentials".format(
            runtime_id=quote(str(runtime_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorEnvelope | ListVncCredentialsResponse:
    if response.status_code == 200:
        response_200 = ListVncCredentialsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorEnvelope.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorEnvelope.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorEnvelope.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorEnvelope.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorEnvelope.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorEnvelope.from_dict(response.json())

        return response_429

    if response.status_code == 501:
        response_501 = ErrorEnvelope.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = ErrorEnvelope.from_dict(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ErrorEnvelope.from_dict(response.json())

        return response_504

    response_default = ErrorEnvelope.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorEnvelope | ListVncCredentialsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorEnvelope | ListVncCredentialsResponse]:
    """List runtime VNC credentials

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | ListVncCredentialsResponse]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorEnvelope | ListVncCredentialsResponse | None:
    """List runtime VNC credentials

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | ListVncCredentialsResponse
    """

    return sync_detailed(
        runtime_id=runtime_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorEnvelope | ListVncCredentialsResponse]:
    """List runtime VNC credentials

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorEnvelope | ListVncCredentialsResponse]
    """

    kwargs = _get_kwargs(
        runtime_id=runtime_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    runtime_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorEnvelope | ListVncCredentialsResponse | None:
    """List runtime VNC credentials

    Args:
        runtime_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorEnvelope | ListVncCredentialsResponse
    """

    return (
        await asyncio_detailed(
            runtime_id=runtime_id,
            client=client,
        )
    ).parsed
