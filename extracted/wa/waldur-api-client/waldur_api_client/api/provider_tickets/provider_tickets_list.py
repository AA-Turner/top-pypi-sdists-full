from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.provider_ticket import ProviderTicket
from ...models.provider_ticket_o_enum import ProviderTicketOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    is_escalated: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ProviderTicketOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    priority: Union[Unset, str] = UNSET,
    provider_assignee: Union[Unset, UUID] = UNSET,
    sla_breached: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    summary: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_escalated"] = is_escalated

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["priority"] = priority

    json_provider_assignee: Union[Unset, str] = UNSET
    if not isinstance(provider_assignee, Unset):
        json_provider_assignee = str(provider_assignee)
    params["provider_assignee"] = json_provider_assignee

    params["sla_breached"] = sla_breached

    params["status"] = status

    params["summary"] = summary

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/provider-tickets/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["ProviderTicket"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProviderTicket.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ProviderTicket"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    is_escalated: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ProviderTicketOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    priority: Union[Unset, str] = UNSET,
    provider_assignee: Union[Unset, UUID] = UNSET,
    sla_breached: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    summary: Union[Unset, str] = UNSET,
) -> Response[list["ProviderTicket"]]:
    """
    Args:
        is_escalated (Union[Unset, bool]):
        o (Union[Unset, list[ProviderTicketOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        priority (Union[Unset, str]):
        provider_assignee (Union[Unset, UUID]):
        sla_breached (Union[Unset, bool]):
        status (Union[Unset, str]):
        summary (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProviderTicket']]
    """

    kwargs = _get_kwargs(
        is_escalated=is_escalated,
        o=o,
        page=page,
        page_size=page_size,
        priority=priority,
        provider_assignee=provider_assignee,
        sla_breached=sla_breached,
        status=status,
        summary=summary,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_escalated: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ProviderTicketOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    priority: Union[Unset, str] = UNSET,
    provider_assignee: Union[Unset, UUID] = UNSET,
    sla_breached: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    summary: Union[Unset, str] = UNSET,
) -> list["ProviderTicket"]:
    """
    Args:
        is_escalated (Union[Unset, bool]):
        o (Union[Unset, list[ProviderTicketOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        priority (Union[Unset, str]):
        provider_assignee (Union[Unset, UUID]):
        sla_breached (Union[Unset, bool]):
        status (Union[Unset, str]):
        summary (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProviderTicket']
    """

    return sync_detailed(
        client=client,
        is_escalated=is_escalated,
        o=o,
        page=page,
        page_size=page_size,
        priority=priority,
        provider_assignee=provider_assignee,
        sla_breached=sla_breached,
        status=status,
        summary=summary,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_escalated: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ProviderTicketOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    priority: Union[Unset, str] = UNSET,
    provider_assignee: Union[Unset, UUID] = UNSET,
    sla_breached: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    summary: Union[Unset, str] = UNSET,
) -> Response[list["ProviderTicket"]]:
    """
    Args:
        is_escalated (Union[Unset, bool]):
        o (Union[Unset, list[ProviderTicketOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        priority (Union[Unset, str]):
        provider_assignee (Union[Unset, UUID]):
        sla_breached (Union[Unset, bool]):
        status (Union[Unset, str]):
        summary (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ProviderTicket']]
    """

    kwargs = _get_kwargs(
        is_escalated=is_escalated,
        o=o,
        page=page,
        page_size=page_size,
        priority=priority,
        provider_assignee=provider_assignee,
        sla_breached=sla_breached,
        status=status,
        summary=summary,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_escalated: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ProviderTicketOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    priority: Union[Unset, str] = UNSET,
    provider_assignee: Union[Unset, UUID] = UNSET,
    sla_breached: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    summary: Union[Unset, str] = UNSET,
) -> list["ProviderTicket"]:
    """
    Args:
        is_escalated (Union[Unset, bool]):
        o (Union[Unset, list[ProviderTicketOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        priority (Union[Unset, str]):
        provider_assignee (Union[Unset, UUID]):
        sla_breached (Union[Unset, bool]):
        status (Union[Unset, str]):
        summary (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProviderTicket']
    """

    return (
        await asyncio_detailed(
            client=client,
            is_escalated=is_escalated,
            o=o,
            page=page,
            page_size=page_size,
            priority=priority,
            provider_assignee=provider_assignee,
            sla_breached=sla_breached,
            status=status,
            summary=summary,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    is_escalated: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ProviderTicketOEnum]] = UNSET,
    priority: Union[Unset, str] = UNSET,
    provider_assignee: Union[Unset, UUID] = UNSET,
    sla_breached: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    summary: Union[Unset, str] = UNSET,
) -> list["ProviderTicket"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_escalated (Union[Unset, bool]):
        o (Union[Unset, list[ProviderTicketOEnum]]):
        priority (Union[Unset, str]):
        provider_assignee (Union[Unset, UUID]):
        sla_breached (Union[Unset, bool]):
        status (Union[Unset, str]):
        summary (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProviderTicket']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ProviderTicket] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_escalated=is_escalated,
        o=o,
        priority=priority,
        provider_assignee=provider_assignee,
        sla_breached=sla_breached,
        status=status,
        summary=summary,
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
    is_escalated: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ProviderTicketOEnum]] = UNSET,
    priority: Union[Unset, str] = UNSET,
    provider_assignee: Union[Unset, UUID] = UNSET,
    sla_breached: Union[Unset, bool] = UNSET,
    status: Union[Unset, str] = UNSET,
    summary: Union[Unset, str] = UNSET,
) -> list["ProviderTicket"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        is_escalated (Union[Unset, bool]):
        o (Union[Unset, list[ProviderTicketOEnum]]):
        priority (Union[Unset, str]):
        provider_assignee (Union[Unset, UUID]):
        sla_breached (Union[Unset, bool]):
        status (Union[Unset, str]):
        summary (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ProviderTicket']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ProviderTicket] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        is_escalated=is_escalated,
        o=o,
        priority=priority,
        provider_assignee=provider_assignee,
        sla_breached=sla_breached,
        status=status,
        summary=summary,
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
