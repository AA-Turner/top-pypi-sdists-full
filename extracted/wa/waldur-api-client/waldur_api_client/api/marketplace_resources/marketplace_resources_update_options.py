from http import HTTPStatus
from typing import Any, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order_uuid import OrderUUID
from ...models.resource_options_request import ResourceOptionsRequest
from ...models.resource_response_status import ResourceResponseStatus
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ResourceOptionsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-resources/{uuid}/update_options/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, OrderUUID, ResourceResponseStatus]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ResourceResponseStatus.from_dict(response.json())

        return response_200
    if response.status_code == 201:
        response_201 = OrderUUID.from_dict(response.json())

        return response_201
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, OrderUUID, ResourceResponseStatus]]:
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
    body: ResourceOptionsRequest,
) -> Response[Union[Any, OrderUUID, ResourceResponseStatus]]:
    """Update resource options

     Updates the options of a resource. If the offering is configured to create orders for option
    changes, a new UPDATE order will be created. Otherwise, the options are updated directly.

    Args:
        uuid (UUID):
        body (ResourceOptionsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OrderUUID, ResourceResponseStatus]]
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
    body: ResourceOptionsRequest,
) -> Union[Any, OrderUUID, ResourceResponseStatus]:
    """Update resource options

     Updates the options of a resource. If the offering is configured to create orders for option
    changes, a new UPDATE order will be created. Otherwise, the options are updated directly.

    Args:
        uuid (UUID):
        body (ResourceOptionsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OrderUUID, ResourceResponseStatus]
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
    body: ResourceOptionsRequest,
) -> Response[Union[Any, OrderUUID, ResourceResponseStatus]]:
    """Update resource options

     Updates the options of a resource. If the offering is configured to create orders for option
    changes, a new UPDATE order will be created. Otherwise, the options are updated directly.

    Args:
        uuid (UUID):
        body (ResourceOptionsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OrderUUID, ResourceResponseStatus]]
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
    body: ResourceOptionsRequest,
) -> Union[Any, OrderUUID, ResourceResponseStatus]:
    """Update resource options

     Updates the options of a resource. If the offering is configured to create orders for option
    changes, a new UPDATE order will be created. Otherwise, the options are updated directly.

    Args:
        uuid (UUID):
        body (ResourceOptionsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OrderUUID, ResourceResponseStatus]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
