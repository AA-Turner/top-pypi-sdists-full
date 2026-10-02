from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.remote_project import RemoteProject
from ...models.remote_project_state_enum import RemoteProjectStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    destination: Union[Unset, str] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["customer"] = customer

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["destination"] = destination

    params["identifier"] = identifier

    params["o"] = o

    params["page"] = page

    params["page_size"] = page_size

    params["project"] = project

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["query"] = query

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/openportal-remote-projects/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["RemoteProject"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RemoteProject.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["RemoteProject"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    destination: Union[Unset, str] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectStateEnum]] = UNSET,
) -> Response[list["RemoteProject"]]:
    """
    Args:
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        destination (Union[Unset, str]):
        identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RemoteProject']]
    """

    kwargs = _get_kwargs(
        customer=customer,
        customer_uuid=customer_uuid,
        destination=destination,
        identifier=identifier,
        o=o,
        page=page,
        page_size=page_size,
        project=project,
        project_uuid=project_uuid,
        query=query,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    destination: Union[Unset, str] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectStateEnum]] = UNSET,
) -> list["RemoteProject"]:
    """
    Args:
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        destination (Union[Unset, str]):
        identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RemoteProject']
    """

    return sync_detailed(
        client=client,
        customer=customer,
        customer_uuid=customer_uuid,
        destination=destination,
        identifier=identifier,
        o=o,
        page=page,
        page_size=page_size,
        project=project,
        project_uuid=project_uuid,
        query=query,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    destination: Union[Unset, str] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectStateEnum]] = UNSET,
) -> Response[list["RemoteProject"]]:
    """
    Args:
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        destination (Union[Unset, str]):
        identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['RemoteProject']]
    """

    kwargs = _get_kwargs(
        customer=customer,
        customer_uuid=customer_uuid,
        destination=destination,
        identifier=identifier,
        o=o,
        page=page,
        page_size=page_size,
        project=project,
        project_uuid=project_uuid,
        query=query,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    destination: Union[Unset, str] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectStateEnum]] = UNSET,
) -> list["RemoteProject"]:
    """
    Args:
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        destination (Union[Unset, str]):
        identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RemoteProject']
    """

    return (
        await asyncio_detailed(
            client=client,
            customer=customer,
            customer_uuid=customer_uuid,
            destination=destination,
            identifier=identifier,
            o=o,
            page=page,
            page_size=page_size,
            project=project,
            project_uuid=project_uuid,
            query=query,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    destination: Union[Unset, str] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectStateEnum]] = UNSET,
) -> list["RemoteProject"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        destination (Union[Unset, str]):
        identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RemoteProject']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RemoteProject] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer=customer,
        customer_uuid=customer_uuid,
        destination=destination,
        identifier=identifier,
        o=o,
        project=project,
        project_uuid=project_uuid,
        query=query,
        state=state,
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
    customer: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    destination: Union[Unset, str] = UNSET,
    identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectStateEnum]] = UNSET,
) -> list["RemoteProject"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        destination (Union[Unset, str]):
        identifier (Union[Unset, str]):
        o (Union[Unset, str]):
        project (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['RemoteProject']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[RemoteProject] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        customer=customer,
        customer_uuid=customer_uuid,
        destination=destination,
        identifier=identifier,
        o=o,
        project=project,
        project_uuid=project_uuid,
        query=query,
        state=state,
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
