from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.expertise_category import ExpertiseCategory
from ...models.expertise_category_o_enum import ExpertiseCategoryOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["code"] = code

    params["level"] = level

    params["name"] = name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_parent_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_uuid, Unset):
        json_parent_uuid = str(parent_uuid)
    params["parent_uuid"] = json_parent_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/expertise-categories/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ExpertiseCategory"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExpertiseCategory.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ExpertiseCategory"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ExpertiseCategory"]]:
    """
    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ExpertiseCategory']]
    """

    kwargs = _get_kwargs(
        code=code,
        level=level,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> list["ExpertiseCategory"]:
    """
    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ExpertiseCategory']
    """

    return sync_detailed(
        client=client,
        code=code,
        level=level,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ExpertiseCategory"]]:
    """
    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ExpertiseCategory']]
    """

    kwargs = _get_kwargs(
        code=code,
        level=level,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> list["ExpertiseCategory"]:
    """
    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ExpertiseCategory']
    """

    return (
        await asyncio_detailed(
            client=client,
            code=code,
            level=level,
            name=name,
            o=o,
            page=page,
            page_size=page_size,
            parent_uuid=parent_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> list["ExpertiseCategory"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ExpertiseCategory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ExpertiseCategory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        code=code,
        level=level,
        name=name,
        o=o,
        parent_uuid=parent_uuid,
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
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> list["ExpertiseCategory"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ExpertiseCategory']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ExpertiseCategory] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        code=code,
        level=level,
        name=name,
        o=o,
        parent_uuid=parent_uuid,
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
