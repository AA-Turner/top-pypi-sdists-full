import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.campaign import Campaign
from ...models.campaign_o_enum import CampaignOEnum
from ...models.campaign_state_enum import CampaignStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    discount_type: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[CampaignOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[CampaignStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["discount_type"] = discount_type

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["offering"] = offering

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["query"] = query

    json_service_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_provider_uuid, Unset):
        json_service_provider_uuid = str(service_provider_uuid)
    params["service_provider_uuid"] = json_service_provider_uuid

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

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
        "url": "/api/promotions-campaigns/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["Campaign"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Campaign.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Campaign"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    discount_type: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[CampaignOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[CampaignStateEnum]] = UNSET,
) -> Response[list["Campaign"]]:
    """
    Args:
        discount_type (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[CampaignOEnum]]):
        offering (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[CampaignStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Campaign']]
    """

    kwargs = _get_kwargs(
        discount_type=discount_type,
        end_date=end_date,
        o=o,
        offering=offering,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        query=query,
        service_provider_uuid=service_provider_uuid,
        start_date=start_date,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    discount_type: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[CampaignOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[CampaignStateEnum]] = UNSET,
) -> list["Campaign"]:
    """
    Args:
        discount_type (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[CampaignOEnum]]):
        offering (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[CampaignStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Campaign']
    """

    return sync_detailed(
        client=client,
        discount_type=discount_type,
        end_date=end_date,
        o=o,
        offering=offering,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        query=query,
        service_provider_uuid=service_provider_uuid,
        start_date=start_date,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    discount_type: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[CampaignOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[CampaignStateEnum]] = UNSET,
) -> Response[list["Campaign"]]:
    """
    Args:
        discount_type (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[CampaignOEnum]]):
        offering (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[CampaignStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Campaign']]
    """

    kwargs = _get_kwargs(
        discount_type=discount_type,
        end_date=end_date,
        o=o,
        offering=offering,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        query=query,
        service_provider_uuid=service_provider_uuid,
        start_date=start_date,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    discount_type: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[CampaignOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[CampaignStateEnum]] = UNSET,
) -> list["Campaign"]:
    """
    Args:
        discount_type (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[CampaignOEnum]]):
        offering (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[CampaignStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Campaign']
    """

    return (
        await asyncio_detailed(
            client=client,
            discount_type=discount_type,
            end_date=end_date,
            o=o,
            offering=offering,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            query=query,
            service_provider_uuid=service_provider_uuid,
            start_date=start_date,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    discount_type: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[CampaignOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[CampaignStateEnum]] = UNSET,
) -> list["Campaign"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        discount_type (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[CampaignOEnum]]):
        offering (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[CampaignStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Campaign']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Campaign] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        discount_type=discount_type,
        end_date=end_date,
        o=o,
        offering=offering,
        offering_uuid=offering_uuid,
        query=query,
        service_provider_uuid=service_provider_uuid,
        start_date=start_date,
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
    discount_type: Union[Unset, str] = UNSET,
    end_date: Union[Unset, datetime.date] = UNSET,
    o: Union[Unset, list[CampaignOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    start_date: Union[Unset, datetime.date] = UNSET,
    state: Union[Unset, list[CampaignStateEnum]] = UNSET,
) -> list["Campaign"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        discount_type (Union[Unset, str]):
        end_date (Union[Unset, datetime.date]):
        o (Union[Unset, list[CampaignOEnum]]):
        offering (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        start_date (Union[Unset, datetime.date]):
        state (Union[Unset, list[CampaignStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Campaign']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Campaign] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        discount_type=discount_type,
        end_date=end_date,
        o=o,
        offering=offering,
        offering_uuid=offering_uuid,
        query=query,
        service_provider_uuid=service_provider_uuid,
        start_date=start_date,
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
