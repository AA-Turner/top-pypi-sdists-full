import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.service_provider_project_group import ServiceProviderProjectGroup
from ...models.service_provider_project_group_o_enum import ServiceProviderProjectGroupOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    gid: Union[Unset, int] = UNSET,
    in_use: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ServiceProviderProjectGroupOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["created_before"] = json_created_before

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["gid"] = gid

    params["in_use"] = in_use

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    json_modified_before: Union[Unset, str] = UNSET
    if not isinstance(modified_before, Unset):
        json_modified_before = modified_before.isoformat()
    params["modified_before"] = json_modified_before

    params["name"] = name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    json_provider_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_offering_uuid, Unset):
        json_provider_offering_uuid = str(provider_offering_uuid)
    params["provider_offering_uuid"] = json_provider_offering_uuid

    params["query"] = query

    json_service_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_provider_uuid, Unset):
        json_service_provider_uuid = str(service_provider_uuid)
    params["service_provider_uuid"] = json_service_provider_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-service-provider-project-groups/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ServiceProviderProjectGroup"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ServiceProviderProjectGroup.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ServiceProviderProjectGroup"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    gid: Union[Unset, int] = UNSET,
    in_use: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ServiceProviderProjectGroupOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ServiceProviderProjectGroup"]]:
    """
    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        gid (Union[Unset, int]):
        in_use (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ServiceProviderProjectGroupOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ServiceProviderProjectGroup']]
    """

    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        gid=gid,
        in_use=in_use,
        modified=modified,
        modified_before=modified_before,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        provider_offering_uuid=provider_offering_uuid,
        query=query,
        service_provider_uuid=service_provider_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    gid: Union[Unset, int] = UNSET,
    in_use: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ServiceProviderProjectGroupOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["ServiceProviderProjectGroup"]:
    """
    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        gid (Union[Unset, int]):
        in_use (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ServiceProviderProjectGroupOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderProjectGroup']
    """

    return sync_detailed(
        client=client,
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        gid=gid,
        in_use=in_use,
        modified=modified,
        modified_before=modified_before,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        provider_offering_uuid=provider_offering_uuid,
        query=query,
        service_provider_uuid=service_provider_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    gid: Union[Unset, int] = UNSET,
    in_use: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ServiceProviderProjectGroupOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["ServiceProviderProjectGroup"]]:
    """
    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        gid (Union[Unset, int]):
        in_use (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ServiceProviderProjectGroupOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ServiceProviderProjectGroup']]
    """

    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        gid=gid,
        in_use=in_use,
        modified=modified,
        modified_before=modified_before,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        project_uuid=project_uuid,
        provider_offering_uuid=provider_offering_uuid,
        query=query,
        service_provider_uuid=service_provider_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    gid: Union[Unset, int] = UNSET,
    in_use: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ServiceProviderProjectGroupOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["ServiceProviderProjectGroup"]:
    """
    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        gid (Union[Unset, int]):
        in_use (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ServiceProviderProjectGroupOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_uuid (Union[Unset, UUID]):
        provider_offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderProjectGroup']
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            created_before=created_before,
            customer_uuid=customer_uuid,
            gid=gid,
            in_use=in_use,
            modified=modified,
            modified_before=modified_before,
            name=name,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            project_uuid=project_uuid,
            provider_offering_uuid=provider_offering_uuid,
            query=query,
            service_provider_uuid=service_provider_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    gid: Union[Unset, int] = UNSET,
    in_use: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ServiceProviderProjectGroupOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["ServiceProviderProjectGroup"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        gid (Union[Unset, int]):
        in_use (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ServiceProviderProjectGroupOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderProjectGroup']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ServiceProviderProjectGroup] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        gid=gid,
        in_use=in_use,
        modified=modified,
        modified_before=modified_before,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        provider_offering_uuid=provider_offering_uuid,
        query=query,
        service_provider_uuid=service_provider_uuid,
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
    created: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    gid: Union[Unset, int] = UNSET,
    in_use: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    modified_before: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ServiceProviderProjectGroupOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    provider_offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
) -> list["ServiceProviderProjectGroup"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        customer_uuid (Union[Unset, UUID]):
        gid (Union[Unset, int]):
        in_use (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        modified_before (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ServiceProviderProjectGroupOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        project_uuid (Union[Unset, UUID]):
        provider_offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ServiceProviderProjectGroup']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ServiceProviderProjectGroup] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        created_before=created_before,
        customer_uuid=customer_uuid,
        gid=gid,
        in_use=in_use,
        modified=modified,
        modified_before=modified_before,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        project_uuid=project_uuid,
        provider_offering_uuid=provider_offering_uuid,
        query=query,
        service_provider_uuid=service_provider_uuid,
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
