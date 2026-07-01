from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.workos_auth_code_start_request import WorkosAuthCodeStartRequest
from ...models.workos_auth_code_start_response import WorkosAuthCodeStartResponse
from ...types import Response


def _get_kwargs(
    *,
    body: WorkosAuthCodeStartRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/v1/workos/auth-code/authorization-url",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse400 | WorkosAuthCodeStartResponse | None:
    if response.status_code == 201:
        response_201 = WorkosAuthCodeStartResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse400 | WorkosAuthCodeStartResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: WorkosAuthCodeStartRequest,
) -> Response[ErrorResponse400 | WorkosAuthCodeStartResponse]:
    """WorkosAuthCodeStart

    Args:
        body (WorkosAuthCodeStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | WorkosAuthCodeStartResponse]
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
    client: AuthenticatedClient | Client,
    body: WorkosAuthCodeStartRequest,
) -> ErrorResponse400 | WorkosAuthCodeStartResponse | None:
    """WorkosAuthCodeStart

    Args:
        body (WorkosAuthCodeStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | WorkosAuthCodeStartResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: WorkosAuthCodeStartRequest,
) -> Response[ErrorResponse400 | WorkosAuthCodeStartResponse]:
    """WorkosAuthCodeStart

    Args:
        body (WorkosAuthCodeStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse400 | WorkosAuthCodeStartResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: WorkosAuthCodeStartRequest,
) -> ErrorResponse400 | WorkosAuthCodeStartResponse | None:
    """WorkosAuthCodeStart

    Args:
        body (WorkosAuthCodeStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse400 | WorkosAuthCodeStartResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
