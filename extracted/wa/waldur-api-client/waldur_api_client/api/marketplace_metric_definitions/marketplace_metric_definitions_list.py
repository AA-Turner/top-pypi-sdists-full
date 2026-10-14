from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_definition import MetricDefinition
from ...models.metric_definition_state_enum import MetricDefinitionStateEnum
from ...models.metric_kind_enum import MetricKindEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_global"] = is_global

    params["key"] = key

    json_kind: Union[Unset, str] = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    params["name"] = name

    json_owner_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(owner_customer_uuid, Unset):
        json_owner_customer_uuid = str(owner_customer_uuid)
    params["owner_customer_uuid"] = json_owner_customer_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-metric-definitions/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["MetricDefinition"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MetricDefinition.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["MetricDefinition"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> Response[list["MetricDefinition"]]:
    """
    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MetricDefinition']]
    """

    kwargs = _get_kwargs(
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> list["MetricDefinition"]:
    """
    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricDefinition']
    """

    return sync_detailed(
        client=client,
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
        page=page,
        page_size=page_size,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> Response[list["MetricDefinition"]]:
    """
    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MetricDefinition']]
    """

    kwargs = _get_kwargs(
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> list["MetricDefinition"]:
    """
    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricDefinition']
    """

    return (
        await asyncio_detailed(
            client=client,
            is_global=is_global,
            key=key,
            kind=kind,
            name=name,
            owner_customer_uuid=owner_customer_uuid,
            page=page,
            page_size=page_size,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> list["MetricDefinition"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricDefinition']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MetricDefinition] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
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
    is_global: Union[Unset, bool] = UNSET,
    key: Union[Unset, str] = UNSET,
    kind: Union[Unset, MetricKindEnum] = UNSET,
    name: Union[Unset, str] = UNSET,
    owner_customer_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, MetricDefinitionStateEnum] = UNSET,
) -> list["MetricDefinition"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_global (Union[Unset, bool]):
        key (Union[Unset, str]):
        kind (Union[Unset, MetricKindEnum]):
        name (Union[Unset, str]):
        owner_customer_uuid (Union[Unset, UUID]):
        state (Union[Unset, MetricDefinitionStateEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MetricDefinition']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MetricDefinition] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_global=is_global,
        key=key,
        kind=kind,
        name=name,
        owner_customer_uuid=owner_customer_uuid,
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
