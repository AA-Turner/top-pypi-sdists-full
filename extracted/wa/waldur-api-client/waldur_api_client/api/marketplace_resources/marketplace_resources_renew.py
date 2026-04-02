from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_uuid import OrderUUID
from ...models.resource_renew_request import ResourceRenewRequest
from ...models.resource_renew_request_form import ResourceRenewRequestForm
from ...models.resource_renew_request_multipart import ResourceRenewRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        ResourceRenewRequest,
        ResourceRenewRequestForm,
        ResourceRenewRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-resources/{uuid}/renew/",
    }

    if isinstance(body, ResourceRenewRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ResourceRenewRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, ResourceRenewRequestMultipart):
        _kwargs["files"] = body.to_multipart()

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
    body: Union[
        ResourceRenewRequest,
        ResourceRenewRequestForm,
        ResourceRenewRequestMultipart,
    ],
) -> Response[OrderUUID]:
    """Renew a prepaid resource

     Creates a renewal order to extend the subscription period of a prepaid resource. Optionally, limits
    can be upgraded at the same time.

    Args:
        uuid (UUID):
        body (ResourceRenewRequest):
        body (ResourceRenewRequestForm):
        body (ResourceRenewRequestMultipart):

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
    body: Union[
        ResourceRenewRequest,
        ResourceRenewRequestForm,
        ResourceRenewRequestMultipart,
    ],
) -> OrderUUID:
    """Renew a prepaid resource

     Creates a renewal order to extend the subscription period of a prepaid resource. Optionally, limits
    can be upgraded at the same time.

    Args:
        uuid (UUID):
        body (ResourceRenewRequest):
        body (ResourceRenewRequestForm):
        body (ResourceRenewRequestMultipart):

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
    body: Union[
        ResourceRenewRequest,
        ResourceRenewRequestForm,
        ResourceRenewRequestMultipart,
    ],
) -> Response[OrderUUID]:
    """Renew a prepaid resource

     Creates a renewal order to extend the subscription period of a prepaid resource. Optionally, limits
    can be upgraded at the same time.

    Args:
        uuid (UUID):
        body (ResourceRenewRequest):
        body (ResourceRenewRequestForm):
        body (ResourceRenewRequestMultipart):

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
    body: Union[
        ResourceRenewRequest,
        ResourceRenewRequestForm,
        ResourceRenewRequestMultipart,
    ],
) -> OrderUUID:
    """Renew a prepaid resource

     Creates a renewal order to extend the subscription period of a prepaid resource. Optionally, limits
    can be upgraded at the same time.

    Args:
        uuid (UUID):
        body (ResourceRenewRequest):
        body (ResourceRenewRequestForm):
        body (ResourceRenewRequestMultipart):

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
