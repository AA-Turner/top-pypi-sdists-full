from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.identity_bridge_request_request import IdentityBridgeRequestRequest
from ...models.identity_bridge_result import IdentityBridgeResult
from ...types import Response


def _get_kwargs(
    *,
    body: IdentityBridgeRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/identity-bridge/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> IdentityBridgeResult:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = IdentityBridgeResult.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[IdentityBridgeResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: IdentityBridgeRequestRequest,
) -> Response[IdentityBridgeResult]:
    """Push user attributes from an ISD

     Allows Identity Service Domains (ISDs) to push user attributes to Waldur. Creates or updates a user
    based on username (CUID). Requires FEDERATED_IDENTITY_SYNC_ENABLED to be True. Caller must be staff
    or an identity manager with the declared source in managed_isds.

    Args:
        body (IdentityBridgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IdentityBridgeResult]
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
    body: IdentityBridgeRequestRequest,
) -> IdentityBridgeResult:
    """Push user attributes from an ISD

     Allows Identity Service Domains (ISDs) to push user attributes to Waldur. Creates or updates a user
    based on username (CUID). Requires FEDERATED_IDENTITY_SYNC_ENABLED to be True. Caller must be staff
    or an identity manager with the declared source in managed_isds.

    Args:
        body (IdentityBridgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IdentityBridgeResult
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: IdentityBridgeRequestRequest,
) -> Response[IdentityBridgeResult]:
    """Push user attributes from an ISD

     Allows Identity Service Domains (ISDs) to push user attributes to Waldur. Creates or updates a user
    based on username (CUID). Requires FEDERATED_IDENTITY_SYNC_ENABLED to be True. Caller must be staff
    or an identity manager with the declared source in managed_isds.

    Args:
        body (IdentityBridgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IdentityBridgeResult]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: IdentityBridgeRequestRequest,
) -> IdentityBridgeResult:
    """Push user attributes from an ISD

     Allows Identity Service Domains (ISDs) to push user attributes to Waldur. Creates or updates a user
    based on username (CUID). Requires FEDERATED_IDENTITY_SYNC_ENABLED to be True. Caller must be staff
    or an identity manager with the declared source in managed_isds.

    Args:
        body (IdentityBridgeRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IdentityBridgeResult
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
