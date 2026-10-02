from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_category import MarketplaceCategory
from ...models.marketplace_category_request import MarketplaceCategoryRequest
from ...models.marketplace_category_request_form import MarketplaceCategoryRequestForm
from ...models.marketplace_category_request_multipart import MarketplaceCategoryRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        MarketplaceCategoryRequest,
        MarketplaceCategoryRequestForm,
        MarketplaceCategoryRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/marketplace-categories/{uuid}/",
    }

    if isinstance(body, MarketplaceCategoryRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, MarketplaceCategoryRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, MarketplaceCategoryRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> MarketplaceCategory:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MarketplaceCategory.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MarketplaceCategory]:
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
        MarketplaceCategoryRequest,
        MarketplaceCategoryRequestForm,
        MarketplaceCategoryRequestMultipart,
    ],
) -> Response[MarketplaceCategory]:
    """Update a category

     Updates an existing marketplace category. Requires staff permissions.

    Args:
        uuid (UUID):
        body (MarketplaceCategoryRequest):
        body (MarketplaceCategoryRequestForm):
        body (MarketplaceCategoryRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceCategory]
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
        MarketplaceCategoryRequest,
        MarketplaceCategoryRequestForm,
        MarketplaceCategoryRequestMultipart,
    ],
) -> MarketplaceCategory:
    """Update a category

     Updates an existing marketplace category. Requires staff permissions.

    Args:
        uuid (UUID):
        body (MarketplaceCategoryRequest):
        body (MarketplaceCategoryRequestForm):
        body (MarketplaceCategoryRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceCategory
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
        MarketplaceCategoryRequest,
        MarketplaceCategoryRequestForm,
        MarketplaceCategoryRequestMultipart,
    ],
) -> Response[MarketplaceCategory]:
    """Update a category

     Updates an existing marketplace category. Requires staff permissions.

    Args:
        uuid (UUID):
        body (MarketplaceCategoryRequest):
        body (MarketplaceCategoryRequestForm):
        body (MarketplaceCategoryRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceCategory]
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
        MarketplaceCategoryRequest,
        MarketplaceCategoryRequestForm,
        MarketplaceCategoryRequestMultipart,
    ],
) -> MarketplaceCategory:
    """Update a category

     Updates an existing marketplace category. Requires staff permissions.

    Args:
        uuid (UUID):
        body (MarketplaceCategoryRequest):
        body (MarketplaceCategoryRequestForm):
        body (MarketplaceCategoryRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceCategory
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
