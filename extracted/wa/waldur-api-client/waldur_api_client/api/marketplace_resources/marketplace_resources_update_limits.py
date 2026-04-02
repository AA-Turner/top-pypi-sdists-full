from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_uuid import OrderUUID
from ...models.resource_update_limits_request import ResourceUpdateLimitsRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ResourceUpdateLimitsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-resources/{uuid}/update_limits/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OrderUUID:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OrderUUID.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[OrderUUID]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceUpdateLimitsRequest,
) -> Response[OrderUUID]:
    """Update resource limits

     Creates a marketplace order to update the limits (e.g., CPU, RAM) for a resource. This action is
    asynchronous and may require approval.

    Args:
        uuid (UUID):
        body (ResourceUpdateLimitsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderUUID]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceUpdateLimitsRequest,
) -> OrderUUID:
    """Update resource limits

     Creates a marketplace order to update the limits (e.g., CPU, RAM) for a resource. This action is
    asynchronous and may require approval.

    Args:
        uuid (UUID):
        body (ResourceUpdateLimitsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderUUID
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceUpdateLimitsRequest,
) -> Response[OrderUUID]:
    """Update resource limits

     Creates a marketplace order to update the limits (e.g., CPU, RAM) for a resource. This action is
    asynchronous and may require approval.

    Args:
        uuid (UUID):
        body (ResourceUpdateLimitsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderUUID]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceUpdateLimitsRequest,
) -> OrderUUID:
    """Update resource limits

     Creates a marketplace order to update the limits (e.g., CPU, RAM) for a resource. This action is
    asynchronous and may require approval.

    Args:
        uuid (UUID):
        body (ResourceUpdateLimitsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderUUID
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
