from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.environment_create_request import EnvironmentCreateRequest
from ...models.environment_response import EnvironmentResponse
from ...models.error_response import ErrorResponse


def _get_kwargs(
    *,
    body: EnvironmentCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/environments",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EnvironmentResponse | ErrorResponse | None:
    if response.status_code == 201:
        response_201 = EnvironmentResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[EnvironmentResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: EnvironmentCreateRequest,
) -> Response[EnvironmentResponse | ErrorResponse]:
    """Create Environment

     Create a new environment. The caller provides the id (key) in the request body.

    Args:
        body (EnvironmentCreateRequest): JSON:API request envelope for creating an environment.

            Distinct from :class:`EnvironmentRequest` because create requires
            caller-supplied ``data.id`` while update does not (the id lives in
            the URL path).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnvironmentResponse | ErrorResponse]
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
    client: AuthenticatedClient,
    body: EnvironmentCreateRequest,
) -> EnvironmentResponse | ErrorResponse | None:
    """Create Environment

     Create a new environment. The caller provides the id (key) in the request body.

    Args:
        body (EnvironmentCreateRequest): JSON:API request envelope for creating an environment.

            Distinct from :class:`EnvironmentRequest` because create requires
            caller-supplied ``data.id`` while update does not (the id lives in
            the URL path).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnvironmentResponse | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: EnvironmentCreateRequest,
) -> Response[EnvironmentResponse | ErrorResponse]:
    """Create Environment

     Create a new environment. The caller provides the id (key) in the request body.

    Args:
        body (EnvironmentCreateRequest): JSON:API request envelope for creating an environment.

            Distinct from :class:`EnvironmentRequest` because create requires
            caller-supplied ``data.id`` while update does not (the id lives in
            the URL path).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnvironmentResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: EnvironmentCreateRequest,
) -> EnvironmentResponse | ErrorResponse | None:
    """Create Environment

     Create a new environment. The caller provides the id (key) in the request body.

    Args:
        body (EnvironmentCreateRequest): JSON:API request envelope for creating an environment.

            Distinct from :class:`EnvironmentRequest` because create requires
            caller-supplied ``data.id`` while update does not (the id lives in
            the URL path).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnvironmentResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
