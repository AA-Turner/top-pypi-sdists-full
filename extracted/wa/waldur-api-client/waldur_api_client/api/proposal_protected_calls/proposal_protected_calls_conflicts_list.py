from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_states import CallStates
from ...models.conflict_of_interest import ConflictOfInterest
from ...models.protected_call_o_enum import ProtectedCallOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    uuid: UUID,
    *,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["customer"] = customer

    params["customer_keyword"] = customer_keyword

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["has_active_round"] = has_active_round

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

    json_offerings_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(offerings_provider_uuid, Unset):
        json_offerings_provider_uuid = str(offerings_provider_uuid)
    params["offerings_provider_uuid"] = json_offerings_provider_uuid

    params["page"] = page

    params["page_size"] = page_size

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
        "url": f"/api/proposal-protected-calls/{uuid}/conflicts/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ConflictOfInterest"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ConflictOfInterest.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ConflictOfInterest"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> Response[list["ConflictOfInterest"]]:
    """List all conflicts of interest detected for this call.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CallStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ConflictOfInterest']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> list["ConflictOfInterest"]:
    """List all conflicts of interest detected for this call.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CallStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
        page=page,
        page_size=page_size,
        state=state,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> Response[list["ConflictOfInterest"]]:
    """List all conflicts of interest detected for this call.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CallStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ConflictOfInterest']]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
        page=page,
        page_size=page_size,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> list["ConflictOfInterest"]:
    """List all conflicts of interest detected for this call.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[CallStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            customer=customer,
            customer_keyword=customer_keyword,
            customer_uuid=customer_uuid,
            has_active_round=has_active_round,
            name=name,
            o=o,
            offering_uuid=offering_uuid,
            offerings_provider_uuid=offerings_provider_uuid,
            page=page,
            page_size=page_size,
            state=state,
        )
    ).parsed


def sync_all(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> list["ConflictOfInterest"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CallStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ConflictOfInterest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
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
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    customer: Union[Unset, str] = UNSET,
    customer_keyword: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    has_active_round: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProtectedCallOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    offerings_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[CallStates]] = UNSET,
) -> list["ConflictOfInterest"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        uuid (UUID):
        customer (Union[Unset, str]):
        customer_keyword (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        has_active_round (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProtectedCallOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        offerings_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[CallStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ConflictOfInterest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ConflictOfInterest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        uuid=uuid,
        customer=customer,
        customer_keyword=customer_keyword,
        customer_uuid=customer_uuid,
        has_active_round=has_active_round,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        offerings_provider_uuid=offerings_provider_uuid,
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
