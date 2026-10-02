from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.plugin_offering_type import PluginOfferingType
from ...types import Response
from ...utils import parse_link_header


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-plugins/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["PluginOfferingType"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PluginOfferingType.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PluginOfferingType"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list["PluginOfferingType"]]:
    """List available marketplace plugins and their components


            Returns a list of all registered marketplace plugins (offering types) and the components
            associated with each. This endpoint is public and does not require authentication.

            Each plugin entry includes:
            - `offering_type`: A unique identifier for the plugin.
            - `components`: A list of components provided by the plugin, each with its `type`, `name`,
    `measured_unit`, and `billing_type`.
            - `available_limits`: A list of component types that support user-defined limits for this
    plugin.


    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PluginOfferingType']]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> list["PluginOfferingType"]:
    """List available marketplace plugins and their components


            Returns a list of all registered marketplace plugins (offering types) and the components
            associated with each. This endpoint is public and does not require authentication.

            Each plugin entry includes:
            - `offering_type`: A unique identifier for the plugin.
            - `components`: A list of components provided by the plugin, each with its `type`, `name`,
    `measured_unit`, and `billing_type`.
            - `available_limits`: A list of component types that support user-defined limits for this
    plugin.


    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PluginOfferingType']
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[list["PluginOfferingType"]]:
    """List available marketplace plugins and their components


            Returns a list of all registered marketplace plugins (offering types) and the components
            associated with each. This endpoint is public and does not require authentication.

            Each plugin entry includes:
            - `offering_type`: A unique identifier for the plugin.
            - `components`: A list of components provided by the plugin, each with its `type`, `name`,
    `measured_unit`, and `billing_type`.
            - `available_limits`: A list of component types that support user-defined limits for this
    plugin.


    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PluginOfferingType']]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> list["PluginOfferingType"]:
    """List available marketplace plugins and their components


            Returns a list of all registered marketplace plugins (offering types) and the components
            associated with each. This endpoint is public and does not require authentication.

            Each plugin entry includes:
            - `offering_type`: A unique identifier for the plugin.
            - `components`: A list of components provided by the plugin, each with its `type`, `name`,
    `measured_unit`, and `billing_type`.
            - `available_limits`: A list of component types that support user-defined limits for this
    plugin.


    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PluginOfferingType']
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed


def sync_all(
    *,
    client: Union[AuthenticatedClient, Client],
) -> list["PluginOfferingType"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PluginOfferingType']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PluginOfferingType] = []

    # Get initial request kwargs
    kwargs = _get_kwargs()

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: Union[AuthenticatedClient, Client],
) -> list["PluginOfferingType"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PluginOfferingType']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PluginOfferingType] = []

    # Get initial request kwargs
    kwargs = _get_kwargs()

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
