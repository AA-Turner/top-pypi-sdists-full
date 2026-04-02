import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.maintenance_announcement import MaintenanceAnnouncement
from ...models.maintenance_announcement_o_enum import MaintenanceAnnouncementOEnum
from ...models.maintenance_announcement_state_enum import MaintenanceAnnouncementStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    maintenance_type: Union[Unset, int] = UNSET,
    o: Union[Unset, list[MaintenanceAnnouncementOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scheduled_end_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_end_before: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_before: Union[Unset, datetime.datetime] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[MaintenanceAnnouncementStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["maintenance_type"] = maintenance_type

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_scheduled_end_after: Union[Unset, str] = UNSET
    if not isinstance(scheduled_end_after, Unset):
        json_scheduled_end_after = scheduled_end_after.isoformat()
    params["scheduled_end_after"] = json_scheduled_end_after

    json_scheduled_end_before: Union[Unset, str] = UNSET
    if not isinstance(scheduled_end_before, Unset):
        json_scheduled_end_before = scheduled_end_before.isoformat()
    params["scheduled_end_before"] = json_scheduled_end_before

    json_scheduled_start_after: Union[Unset, str] = UNSET
    if not isinstance(scheduled_start_after, Unset):
        json_scheduled_start_after = scheduled_start_after.isoformat()
    params["scheduled_start_after"] = json_scheduled_start_after

    json_scheduled_start_before: Union[Unset, str] = UNSET
    if not isinstance(scheduled_start_before, Unset):
        json_scheduled_start_before = scheduled_start_before.isoformat()
    params["scheduled_start_before"] = json_scheduled_start_before

    json_service_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_provider_uuid, Unset):
        json_service_provider_uuid = str(service_provider_uuid)
    params["service_provider_uuid"] = json_service_provider_uuid

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
        "url": "/api/maintenance-announcements/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["MaintenanceAnnouncement"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MaintenanceAnnouncement.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["MaintenanceAnnouncement"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    maintenance_type: Union[Unset, int] = UNSET,
    o: Union[Unset, list[MaintenanceAnnouncementOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scheduled_end_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_end_before: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_before: Union[Unset, datetime.datetime] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[MaintenanceAnnouncementStateEnum]] = UNSET,
) -> Response[list["MaintenanceAnnouncement"]]:
    """List maintenance announcements

     Returns a paginated list of maintenance announcements.

    Args:
        maintenance_type (Union[Unset, int]):
        o (Union[Unset, list[MaintenanceAnnouncementOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scheduled_end_after (Union[Unset, datetime.datetime]):
        scheduled_end_before (Union[Unset, datetime.datetime]):
        scheduled_start_after (Union[Unset, datetime.datetime]):
        scheduled_start_before (Union[Unset, datetime.datetime]):
        service_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[MaintenanceAnnouncementStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MaintenanceAnnouncement']]
    """

    kwargs = _get_kwargs(
        maintenance_type=maintenance_type,
        o=o,
        page=page,
        page_size=page_size,
        scheduled_end_after=scheduled_end_after,
        scheduled_end_before=scheduled_end_before,
        scheduled_start_after=scheduled_start_after,
        scheduled_start_before=scheduled_start_before,
        service_provider_uuid=service_provider_uuid,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    maintenance_type: Union[Unset, int] = UNSET,
    o: Union[Unset, list[MaintenanceAnnouncementOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scheduled_end_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_end_before: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_before: Union[Unset, datetime.datetime] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[MaintenanceAnnouncementStateEnum]] = UNSET,
) -> list["MaintenanceAnnouncement"]:
    """List maintenance announcements

     Returns a paginated list of maintenance announcements.

    Args:
        maintenance_type (Union[Unset, int]):
        o (Union[Unset, list[MaintenanceAnnouncementOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scheduled_end_after (Union[Unset, datetime.datetime]):
        scheduled_end_before (Union[Unset, datetime.datetime]):
        scheduled_start_after (Union[Unset, datetime.datetime]):
        scheduled_start_before (Union[Unset, datetime.datetime]):
        service_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[MaintenanceAnnouncementStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MaintenanceAnnouncement']
    """

    return sync_detailed(
        client=client,
        maintenance_type=maintenance_type,
        o=o,
        page=page,
        page_size=page_size,
        scheduled_end_after=scheduled_end_after,
        scheduled_end_before=scheduled_end_before,
        scheduled_start_after=scheduled_start_after,
        scheduled_start_before=scheduled_start_before,
        service_provider_uuid=service_provider_uuid,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    maintenance_type: Union[Unset, int] = UNSET,
    o: Union[Unset, list[MaintenanceAnnouncementOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scheduled_end_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_end_before: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_before: Union[Unset, datetime.datetime] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[MaintenanceAnnouncementStateEnum]] = UNSET,
) -> Response[list["MaintenanceAnnouncement"]]:
    """List maintenance announcements

     Returns a paginated list of maintenance announcements.

    Args:
        maintenance_type (Union[Unset, int]):
        o (Union[Unset, list[MaintenanceAnnouncementOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scheduled_end_after (Union[Unset, datetime.datetime]):
        scheduled_end_before (Union[Unset, datetime.datetime]):
        scheduled_start_after (Union[Unset, datetime.datetime]):
        scheduled_start_before (Union[Unset, datetime.datetime]):
        service_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[MaintenanceAnnouncementStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['MaintenanceAnnouncement']]
    """

    kwargs = _get_kwargs(
        maintenance_type=maintenance_type,
        o=o,
        page=page,
        page_size=page_size,
        scheduled_end_after=scheduled_end_after,
        scheduled_end_before=scheduled_end_before,
        scheduled_start_after=scheduled_start_after,
        scheduled_start_before=scheduled_start_before,
        service_provider_uuid=service_provider_uuid,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    maintenance_type: Union[Unset, int] = UNSET,
    o: Union[Unset, list[MaintenanceAnnouncementOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scheduled_end_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_end_before: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_before: Union[Unset, datetime.datetime] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[MaintenanceAnnouncementStateEnum]] = UNSET,
) -> list["MaintenanceAnnouncement"]:
    """List maintenance announcements

     Returns a paginated list of maintenance announcements.

    Args:
        maintenance_type (Union[Unset, int]):
        o (Union[Unset, list[MaintenanceAnnouncementOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scheduled_end_after (Union[Unset, datetime.datetime]):
        scheduled_end_before (Union[Unset, datetime.datetime]):
        scheduled_start_after (Union[Unset, datetime.datetime]):
        scheduled_start_before (Union[Unset, datetime.datetime]):
        service_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[MaintenanceAnnouncementStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MaintenanceAnnouncement']
    """

    return (
        await asyncio_detailed(
            client=client,
            maintenance_type=maintenance_type,
            o=o,
            page=page,
            page_size=page_size,
            scheduled_end_after=scheduled_end_after,
            scheduled_end_before=scheduled_end_before,
            scheduled_start_after=scheduled_start_after,
            scheduled_start_before=scheduled_start_before,
            service_provider_uuid=service_provider_uuid,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    maintenance_type: Union[Unset, int] = UNSET,
    o: Union[Unset, list[MaintenanceAnnouncementOEnum]] = UNSET,
    scheduled_end_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_end_before: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_before: Union[Unset, datetime.datetime] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[MaintenanceAnnouncementStateEnum]] = UNSET,
) -> list["MaintenanceAnnouncement"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        maintenance_type (Union[Unset, int]):
        o (Union[Unset, list[MaintenanceAnnouncementOEnum]]):
        scheduled_end_after (Union[Unset, datetime.datetime]):
        scheduled_end_before (Union[Unset, datetime.datetime]):
        scheduled_start_after (Union[Unset, datetime.datetime]):
        scheduled_start_before (Union[Unset, datetime.datetime]):
        service_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[MaintenanceAnnouncementStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MaintenanceAnnouncement']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MaintenanceAnnouncement] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        maintenance_type=maintenance_type,
        o=o,
        scheduled_end_after=scheduled_end_after,
        scheduled_end_before=scheduled_end_before,
        scheduled_start_after=scheduled_start_after,
        scheduled_start_before=scheduled_start_before,
        service_provider_uuid=service_provider_uuid,
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
    maintenance_type: Union[Unset, int] = UNSET,
    o: Union[Unset, list[MaintenanceAnnouncementOEnum]] = UNSET,
    scheduled_end_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_end_before: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_after: Union[Unset, datetime.datetime] = UNSET,
    scheduled_start_before: Union[Unset, datetime.datetime] = UNSET,
    service_provider_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[MaintenanceAnnouncementStateEnum]] = UNSET,
) -> list["MaintenanceAnnouncement"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        maintenance_type (Union[Unset, int]):
        o (Union[Unset, list[MaintenanceAnnouncementOEnum]]):
        scheduled_end_after (Union[Unset, datetime.datetime]):
        scheduled_end_before (Union[Unset, datetime.datetime]):
        scheduled_start_after (Union[Unset, datetime.datetime]):
        scheduled_start_before (Union[Unset, datetime.datetime]):
        service_provider_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[MaintenanceAnnouncementStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['MaintenanceAnnouncement']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[MaintenanceAnnouncement] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        maintenance_type=maintenance_type,
        o=o,
        scheduled_end_after=scheduled_end_after,
        scheduled_end_before=scheduled_end_before,
        scheduled_start_after=scheduled_start_after,
        scheduled_start_before=scheduled_start_before,
        service_provider_uuid=service_provider_uuid,
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
