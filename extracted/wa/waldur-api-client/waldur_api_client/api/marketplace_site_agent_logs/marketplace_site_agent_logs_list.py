from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.site_agent_log import SiteAgentLog
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_agent_identity_uuid: Union[Unset, str] = UNSET
    if not isinstance(agent_identity_uuid, Unset):
        json_agent_identity_uuid = str(agent_identity_uuid)
    params["agent_identity_uuid"] = json_agent_identity_uuid

    params["level"] = level

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["timestamp_from"] = timestamp_from

    params["timestamp_to"] = timestamp_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-site-agent-logs/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["SiteAgentLog"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SiteAgentLog.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["SiteAgentLog"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> Response[list["SiteAgentLog"]]:
    """
    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SiteAgentLog']]
    """

    kwargs = _get_kwargs(
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> list["SiteAgentLog"]:
    """
    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SiteAgentLog']
    """

    return sync_detailed(
        client=client,
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> Response[list["SiteAgentLog"]]:
    """
    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['SiteAgentLog']]
    """

    kwargs = _get_kwargs(
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> list["SiteAgentLog"]:
    """
    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SiteAgentLog']
    """

    return (
        await asyncio_detailed(
            client=client,
            agent_identity_uuid=agent_identity_uuid,
            level=level,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            timestamp_from=timestamp_from,
            timestamp_to=timestamp_to,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> list["SiteAgentLog"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SiteAgentLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SiteAgentLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
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
    agent_identity_uuid: Union[Unset, UUID] = UNSET,
    level: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    timestamp_from: Union[Unset, float] = UNSET,
    timestamp_to: Union[Unset, float] = UNSET,
) -> list["SiteAgentLog"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        agent_identity_uuid (Union[Unset, UUID]):
        level (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        timestamp_from (Union[Unset, float]):
        timestamp_to (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SiteAgentLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SiteAgentLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        agent_identity_uuid=agent_identity_uuid,
        level=level,
        offering_uuid=offering_uuid,
        timestamp_from=timestamp_from,
        timestamp_to=timestamp_to,
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
