from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.lexis_link import LexisLink
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["query"] = query

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    json_uuid: Union[Unset, str] = UNSET
    if not isinstance(uuid, Unset):
        json_uuid = str(uuid)
    params["uuid"] = json_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/lexis-links/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["LexisLink"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = LexisLink.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["LexisLink"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["LexisLink"]]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LexisLink']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        query=query,
        resource_uuid=resource_uuid,
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["LexisLink"]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LexisLink']
    """

    return sync_detailed(
        client=client,
        customer_uuid=customer_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        query=query,
        resource_uuid=resource_uuid,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["LexisLink"]]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LexisLink']]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        query=query,
        resource_uuid=resource_uuid,
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["LexisLink"]:
    """
    Args:
        customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LexisLink']
    """

    return (
        await asyncio_detailed(
            client=client,
            customer_uuid=customer_uuid,
            page=page,
            page_size=page_size,
            project_uuid=project_uuid,
            query=query,
            resource_uuid=resource_uuid,
            uuid=uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    customer_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["LexisLink"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LexisLink']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[LexisLink] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        project_uuid=project_uuid,
        query=query,
        resource_uuid=resource_uuid,
        uuid=uuid,
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
    customer_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,
) -> list["LexisLink"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LexisLink']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[LexisLink] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        project_uuid=project_uuid,
        query=query,
        resource_uuid=resource_uuid,
        uuid=uuid,
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
