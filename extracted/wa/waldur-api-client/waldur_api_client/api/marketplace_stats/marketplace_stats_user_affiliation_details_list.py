from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_affiliation_detail import UserAffiliationDetail
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    category: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["category"] = category

    params["country"] = country

    params["o"] = o

    params["organization"] = organization

    params["page"] = page

    params["page_size"] = page_size

    params["search"] = search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-stats/user_affiliation_details/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["UserAffiliationDetail"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserAffiliationDetail.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["UserAffiliationDetail"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> Response[list["UserAffiliationDetail"]]:
    """Paginated affiliation rows with parsed organization, country, category and identifier fields. Drives
    the affiliation details table; the unparsed aggregate counts remain available via
    user_affiliation_count.

    Args:
        category (Union[Unset, str]):
        country (Union[Unset, str]):
        o (Union[Unset, str]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserAffiliationDetail']]
    """

    kwargs = _get_kwargs(
        category=category,
        country=country,
        o=o,
        organization=organization,
        page=page,
        page_size=page_size,
        search=search,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> list["UserAffiliationDetail"]:
    """Paginated affiliation rows with parsed organization, country, category and identifier fields. Drives
    the affiliation details table; the unparsed aggregate counts remain available via
    user_affiliation_count.

    Args:
        category (Union[Unset, str]):
        country (Union[Unset, str]):
        o (Union[Unset, str]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAffiliationDetail']
    """

    return sync_detailed(
        client=client,
        category=category,
        country=country,
        o=o,
        organization=organization,
        page=page,
        page_size=page_size,
        search=search,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> Response[list["UserAffiliationDetail"]]:
    """Paginated affiliation rows with parsed organization, country, category and identifier fields. Drives
    the affiliation details table; the unparsed aggregate counts remain available via
    user_affiliation_count.

    Args:
        category (Union[Unset, str]):
        country (Union[Unset, str]):
        o (Union[Unset, str]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['UserAffiliationDetail']]
    """

    kwargs = _get_kwargs(
        category=category,
        country=country,
        o=o,
        organization=organization,
        page=page,
        page_size=page_size,
        search=search,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> list["UserAffiliationDetail"]:
    """Paginated affiliation rows with parsed organization, country, category and identifier fields. Drives
    the affiliation details table; the unparsed aggregate counts remain available via
    user_affiliation_count.

    Args:
        category (Union[Unset, str]):
        country (Union[Unset, str]):
        o (Union[Unset, str]):
        organization (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAffiliationDetail']
    """

    return (
        await asyncio_detailed(
            client=client,
            category=category,
            country=country,
            o=o,
            organization=organization,
            page=page,
            page_size=page_size,
            search=search,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> list["UserAffiliationDetail"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        category (Union[Unset, str]):
        country (Union[Unset, str]):
        o (Union[Unset, str]):
        organization (Union[Unset, str]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAffiliationDetail']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserAffiliationDetail] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        category=category,
        country=country,
        o=o,
        organization=organization,
        search=search,
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
    category: Union[Unset, str] = UNSET,
    country: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    organization: Union[Unset, str] = UNSET,
    search: Union[Unset, str] = UNSET,
) -> list["UserAffiliationDetail"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        category (Union[Unset, str]):
        country (Union[Unset, str]):
        o (Union[Unset, str]):
        organization (Union[Unset, str]):
        search (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['UserAffiliationDetail']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[UserAffiliationDetail] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        category=category,
        country=country,
        o=o,
        organization=organization,
        search=search,
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
