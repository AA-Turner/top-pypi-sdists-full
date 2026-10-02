from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_resources_suggest_name_response_200 import MarketplaceResourcesSuggestNameResponse200
from ...models.resource_suggest_name_request import ResourceSuggestNameRequest
from ...types import Response


def _get_kwargs(
    *,
    body: ResourceSuggestNameRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-resources/suggest_name/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MarketplaceResourcesSuggestNameResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MarketplaceResourcesSuggestNameResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MarketplaceResourcesSuggestNameResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ResourceSuggestNameRequest,
) -> Response[MarketplaceResourcesSuggestNameResponse200]:
    """Suggest a resource name

     Generates a suggested name for a new resource based on the project and offering. If the offering has
    a `resource_name_pattern` in `plugin_options`, it is used as a Python format string with variables:
    `{customer_name}`, `{customer_slug}`, `{project_name}`, `{project_slug}`, `{offering_name}`,
    `{offering_slug}`, `{plan_name}`, `{counter}`, and `{attributes[KEY]}` for any order form value.

    Args:
        body (ResourceSuggestNameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceResourcesSuggestNameResponse200]
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
    body: ResourceSuggestNameRequest,
) -> MarketplaceResourcesSuggestNameResponse200:
    """Suggest a resource name

     Generates a suggested name for a new resource based on the project and offering. If the offering has
    a `resource_name_pattern` in `plugin_options`, it is used as a Python format string with variables:
    `{customer_name}`, `{customer_slug}`, `{project_name}`, `{project_slug}`, `{offering_name}`,
    `{offering_slug}`, `{plan_name}`, `{counter}`, and `{attributes[KEY]}` for any order form value.

    Args:
        body (ResourceSuggestNameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceResourcesSuggestNameResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ResourceSuggestNameRequest,
) -> Response[MarketplaceResourcesSuggestNameResponse200]:
    """Suggest a resource name

     Generates a suggested name for a new resource based on the project and offering. If the offering has
    a `resource_name_pattern` in `plugin_options`, it is used as a Python format string with variables:
    `{customer_name}`, `{customer_slug}`, `{project_name}`, `{project_slug}`, `{offering_name}`,
    `{offering_slug}`, `{plan_name}`, `{counter}`, and `{attributes[KEY]}` for any order form value.

    Args:
        body (ResourceSuggestNameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceResourcesSuggestNameResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ResourceSuggestNameRequest,
) -> MarketplaceResourcesSuggestNameResponse200:
    """Suggest a resource name

     Generates a suggested name for a new resource based on the project and offering. If the offering has
    a `resource_name_pattern` in `plugin_options`, it is used as a Python format string with variables:
    `{customer_name}`, `{customer_slug}`, `{project_name}`, `{project_slug}`, `{offering_name}`,
    `{offering_slug}`, `{plan_name}`, `{counter}`, and `{attributes[KEY]}` for any order form value.

    Args:
        body (ResourceSuggestNameRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceResourcesSuggestNameResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
