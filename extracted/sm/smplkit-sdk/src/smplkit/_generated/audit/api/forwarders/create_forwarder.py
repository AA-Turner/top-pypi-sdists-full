from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.forwarder_create_request import ForwarderCreateRequest
from ...models.forwarder_response import ForwarderResponse


def _get_kwargs(
    *,
    body: ForwarderCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/forwarders",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ForwarderResponse | None:
    if response.status_code == 201:
        response_201 = ForwarderResponse.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ForwarderResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ForwarderCreateRequest,
) -> Response[ForwarderResponse]:
    """Create Forwarder

     Create a forwarder for this account.

    The caller supplies the forwarder's key as `data.id`. Keys are
    unique within an account and immutable for the lifetime of the
    forwarder.

    Enablement is per-environment: a forwarder is enabled in an
    environment only via `environments[<env>].enabled`; the base `enabled`
    is always false. Every environment referenced in `environments` must
    exist and be managed for the account.

    Args:
        body (ForwarderCreateRequest): JSON:API request envelope for creating a forwarder.

            Distinct from :class:`ForwarderRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderResponse]
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
    body: ForwarderCreateRequest,
) -> ForwarderResponse | None:
    """Create Forwarder

     Create a forwarder for this account.

    The caller supplies the forwarder's key as `data.id`. Keys are
    unique within an account and immutable for the lifetime of the
    forwarder.

    Enablement is per-environment: a forwarder is enabled in an
    environment only via `environments[<env>].enabled`; the base `enabled`
    is always false. Every environment referenced in `environments` must
    exist and be managed for the account.

    Args:
        body (ForwarderCreateRequest): JSON:API request envelope for creating a forwarder.

            Distinct from :class:`ForwarderRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ForwarderCreateRequest,
) -> Response[ForwarderResponse]:
    """Create Forwarder

     Create a forwarder for this account.

    The caller supplies the forwarder's key as `data.id`. Keys are
    unique within an account and immutable for the lifetime of the
    forwarder.

    Enablement is per-environment: a forwarder is enabled in an
    environment only via `environments[<env>].enabled`; the base `enabled`
    is always false. Every environment referenced in `environments` must
    exist and be managed for the account.

    Args:
        body (ForwarderCreateRequest): JSON:API request envelope for creating a forwarder.

            Distinct from :class:`ForwarderRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ForwarderCreateRequest,
) -> ForwarderResponse | None:
    """Create Forwarder

     Create a forwarder for this account.

    The caller supplies the forwarder's key as `data.id`. Keys are
    unique within an account and immutable for the lifetime of the
    forwarder.

    Enablement is per-environment: a forwarder is enabled in an
    environment only via `environments[<env>].enabled`; the base `enabled`
    is always false. Every environment referenced in `environments` must
    exist and be managed for the account.

    Args:
        body (ForwarderCreateRequest): JSON:API request envelope for creating a forwarder.

            Distinct from :class:`ForwarderRequest` because create requires
            caller-supplied ``data.id`` while update does not.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
