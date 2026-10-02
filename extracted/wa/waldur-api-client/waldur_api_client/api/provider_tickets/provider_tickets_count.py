from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.provider_ticket_o_enum import ProviderTicketOEnum
from ...types import UNSET, Response, Unset


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
        "method": "head",
        "url": "/api/provider-tickets/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
