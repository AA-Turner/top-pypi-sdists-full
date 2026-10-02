from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.affiliated_organization import AffiliatedOrganization
from ...models.affiliated_organization_field_enum import AffiliatedOrganizationFieldEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    abbreviation: Union[Unset, str] = UNSET,
    code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    default_for_customer: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[AffiliatedOrganizationFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["abbreviation"] = abbreviation

    params["code"] = code

    params["country"] = country

    json_default_for_customer: Union[Unset, str] = UNSET
    if not isinstance(default_for_customer, Unset):
        json_default_for_customer = str(default_for_customer)
    params["default_for_customer"] = json_default_for_customer

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["name"] = name

    params["name_exact"] = name_exact

    params["o"] = o

    params["page"] = page

    params["page_size"] = page_size

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/affiliated-organizations/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["AffiliatedOrganization"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AffiliatedOrganization.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AffiliatedOrganization"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    default_for_customer: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[AffiliatedOrganizationFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[list["AffiliatedOrganization"]]:
    """
    Args:
        abbreviation (Union[Unset, str]):
        code (Union[Unset, str]):
        country (Union[Unset, str]):
        default_for_customer (Union[Unset, UUID]):
        field (Union[Unset, list[AffiliatedOrganizationFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AffiliatedOrganization']]
    """

    kwargs = _get_kwargs(
        abbreviation=abbreviation,
        code=code,
        country=country,
        default_for_customer=default_for_customer,
        field=field,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    default_for_customer: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[AffiliatedOrganizationFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> list["AffiliatedOrganization"]:
    """
    Args:
        abbreviation (Union[Unset, str]):
        code (Union[Unset, str]):
        country (Union[Unset, str]):
        default_for_customer (Union[Unset, UUID]):
        field (Union[Unset, list[AffiliatedOrganizationFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AffiliatedOrganization']
    """

    return sync_detailed(
        client=client,
        abbreviation=abbreviation,
        code=code,
        country=country,
        default_for_customer=default_for_customer,
        field=field,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    default_for_customer: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[AffiliatedOrganizationFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[list["AffiliatedOrganization"]]:
    """
    Args:
        abbreviation (Union[Unset, str]):
        code (Union[Unset, str]):
        country (Union[Unset, str]):
        default_for_customer (Union[Unset, UUID]):
        field (Union[Unset, list[AffiliatedOrganizationFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AffiliatedOrganization']]
    """

    kwargs = _get_kwargs(
        abbreviation=abbreviation,
        code=code,
        country=country,
        default_for_customer=default_for_customer,
        field=field,
        name=name,
        name_exact=name_exact,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    default_for_customer: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[AffiliatedOrganizationFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> list["AffiliatedOrganization"]:
    """
    Args:
        abbreviation (Union[Unset, str]):
        code (Union[Unset, str]):
        country (Union[Unset, str]):
        default_for_customer (Union[Unset, UUID]):
        field (Union[Unset, list[AffiliatedOrganizationFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AffiliatedOrganization']
    """

    return (
        await asyncio_detailed(
            client=client,
            abbreviation=abbreviation,
            code=code,
            country=country,
            default_for_customer=default_for_customer,
            field=field,
            name=name,
            name_exact=name_exact,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    abbreviation: Union[Unset, str] = UNSET,
    code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    default_for_customer: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[AffiliatedOrganizationFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> list["AffiliatedOrganization"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        abbreviation (Union[Unset, str]):
        code (Union[Unset, str]):
        country (Union[Unset, str]):
        default_for_customer (Union[Unset, UUID]):
        field (Union[Unset, list[AffiliatedOrganizationFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, str]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AffiliatedOrganization']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AffiliatedOrganization] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        abbreviation=abbreviation,
        code=code,
        country=country,
        default_for_customer=default_for_customer,
        field=field,
        name=name,
        name_exact=name_exact,
        o=o,
        query=query,
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
    abbreviation: Union[Unset, str] = UNSET,
    code: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    default_for_customer: Union[Unset, UUID] = UNSET,
    field: Union[Unset, list[AffiliatedOrganizationFieldEnum]] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> list["AffiliatedOrganization"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        abbreviation (Union[Unset, str]):
        code (Union[Unset, str]):
        country (Union[Unset, str]):
        default_for_customer (Union[Unset, UUID]):
        field (Union[Unset, list[AffiliatedOrganizationFieldEnum]]):
        name (Union[Unset, str]):
        name_exact (Union[Unset, str]):
        o (Union[Unset, str]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AffiliatedOrganization']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AffiliatedOrganization] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        abbreviation=abbreviation,
        code=code,
        country=country,
        default_for_customer=default_for_customer,
        field=field,
        name=name,
        name_exact=name_exact,
        o=o,
        query=query,
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
