from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.forwarder_type_list_response import ForwarderTypeListResponse


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/forwarder_types",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ForwarderTypeListResponse | None:
    if response.status_code == 200:
        response_200 = ForwarderTypeListResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ForwarderTypeListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ForwarderTypeListResponse]:
    """List Forwarder Types

     List all forwarder types in the catalog.

    Returns every branded HTTP forwarder type defined in
    `forwarder_types/*.yaml` plus the synthetic `http` (Custom HTTP) entry.
    The response drives the console's create-forwarder UX, the docs
    vendor-reference page, and audit's own server-side template validation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderTypeListResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ForwarderTypeListResponse | None:
    """List Forwarder Types

     List all forwarder types in the catalog.

    Returns every branded HTTP forwarder type defined in
    `forwarder_types/*.yaml` plus the synthetic `http` (Custom HTTP) entry.
    The response drives the console's create-forwarder UX, the docs
    vendor-reference page, and audit's own server-side template validation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderTypeListResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ForwarderTypeListResponse]:
    """List Forwarder Types

     List all forwarder types in the catalog.

    Returns every branded HTTP forwarder type defined in
    `forwarder_types/*.yaml` plus the synthetic `http` (Custom HTTP) entry.
    The response drives the console's create-forwarder UX, the docs
    vendor-reference page, and audit's own server-side template validation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderTypeListResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ForwarderTypeListResponse | None:
    """List Forwarder Types

     List all forwarder types in the catalog.

    Returns every branded HTTP forwarder type defined in
    `forwarder_types/*.yaml` plus the synthetic `http` (Custom HTTP) entry.
    The response drives the console's create-forwarder UX, the docs
    vendor-reference page, and audit's own server-side template validation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderTypeListResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
