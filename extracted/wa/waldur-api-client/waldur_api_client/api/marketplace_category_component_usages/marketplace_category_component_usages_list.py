import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_component_usage import CategoryComponentUsage
from ...models.category_component_usage_field_enum import CategoryComponentUsageFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_date_after: Union[Unset, str] = UNSET
    if not isinstance(date_after, Unset):
        json_date_after = date_after.isoformat()
    params["date_after"] = json_date_after

    json_date_before: Union[Unset, str] = UNSET
    if not isinstance(date_before, Unset):
        json_date_before = date_before.isoformat()
    params["date_before"] = json_date_before

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["page"] = page

    params["page_size"] = page_size

    params["scope"] = scope

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-category-component-usages/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["CategoryComponentUsage"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CategoryComponentUsage.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["CategoryComponentUsage"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
) -> Response[list["CategoryComponentUsage"]]:
    """List aggregated category component usages


            Returns a paginated list of aggregated component usages for marketplace categories.
            This data is scoped to either a customer or a project and represents the total usage
            of a component type (e.g., total 'CPU hours' used across all resources of a certain category
            within a project).

            The list **must** be filtered by a `scope` parameter (either a customer or project URL).


    Args:
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CategoryComponentUsage']]
    """

    kwargs = _get_kwargs(
        date_after=date_after,
        date_before=date_before,
        field=field,
        page=page,
        page_size=page_size,
        scope=scope,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
) -> list["CategoryComponentUsage"]:
    """List aggregated category component usages


            Returns a paginated list of aggregated component usages for marketplace categories.
            This data is scoped to either a customer or a project and represents the total usage
            of a component type (e.g., total 'CPU hours' used across all resources of a certain category
            within a project).

            The list **must** be filtered by a `scope` parameter (either a customer or project URL).


    Args:
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CategoryComponentUsage']
    """

    return sync_detailed(
        client=client,
        date_after=date_after,
        date_before=date_before,
        field=field,
        page=page,
        page_size=page_size,
        scope=scope,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
) -> Response[list["CategoryComponentUsage"]]:
    """List aggregated category component usages


            Returns a paginated list of aggregated component usages for marketplace categories.
            This data is scoped to either a customer or a project and represents the total usage
            of a component type (e.g., total 'CPU hours' used across all resources of a certain category
            within a project).

            The list **must** be filtered by a `scope` parameter (either a customer or project URL).


    Args:
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CategoryComponentUsage']]
    """

    kwargs = _get_kwargs(
        date_after=date_after,
        date_before=date_before,
        field=field,
        page=page,
        page_size=page_size,
        scope=scope,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
) -> list["CategoryComponentUsage"]:
    """List aggregated category component usages


            Returns a paginated list of aggregated component usages for marketplace categories.
            This data is scoped to either a customer or a project and represents the total usage
            of a component type (e.g., total 'CPU hours' used across all resources of a certain category
            within a project).

            The list **must** be filtered by a `scope` parameter (either a customer or project URL).


    Args:
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CategoryComponentUsage']
    """

    return (
        await asyncio_detailed(
            client=client,
            date_after=date_after,
            date_before=date_before,
            field=field,
            page=page,
            page_size=page_size,
            scope=scope,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
    scope: Union[Unset, str] = UNSET,
) -> list["CategoryComponentUsage"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):
        scope (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CategoryComponentUsage']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[CategoryComponentUsage] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        date_after=date_after,
        date_before=date_before,
        field=field,
        scope=scope,
    )

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
    client: AuthenticatedClient,
    date_after: Union[Unset, datetime.date] = UNSET,
    date_before: Union[Unset, datetime.date] = UNSET,
    field: Union[Unset, list[CategoryComponentUsageFieldEnum]] = UNSET,
    scope: Union[Unset, str] = UNSET,
) -> list["CategoryComponentUsage"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        date_after (Union[Unset, datetime.date]):
        date_before (Union[Unset, datetime.date]):
        field (Union[Unset, list[CategoryComponentUsageFieldEnum]]):
        scope (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CategoryComponentUsage']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[CategoryComponentUsage] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        date_after=date_after,
        date_before=date_before,
        field=field,
        scope=scope,
    )

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
