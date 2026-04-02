import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_user import OfferingUser
from ...models.offering_user_field_enum import OfferingUserFieldEnum
from ...models.offering_user_o_enum import OfferingUserOEnum
from ...models.offering_user_state import OfferingUserState
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created: Union[Unset, datetime.datetime] = UNSET,
    field: Union[Unset, list[OfferingUserFieldEnum]] = UNSET,
    has_complete_profile: Union[Unset, bool] = UNSET,
    has_consent: Union[Unset, bool] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created: Union[Unset, str] = UNSET
    if not isinstance(created, Unset):
        json_created = created.isoformat()
    params["created"] = json_created

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["has_complete_profile"] = has_complete_profile

    params["has_consent"] = has_consent

    params["is_restricted"] = is_restricted

    json_modified: Union[Unset, str] = UNSET
    if not isinstance(modified, Unset):
        json_modified = modified.isoformat()
    params["modified"] = json_modified

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["offering"] = offering

    json_offering_slug: Union[Unset, list[str]] = UNSET
    if not isinstance(offering_slug, Unset):
        json_offering_slug = offering_slug

    params["offering_slug"] = json_offering_slug

    json_offering_uuid: Union[Unset, list[str]] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = []
        for offering_uuid_item_data in offering_uuid:
            offering_uuid_item = str(offering_uuid_item_data)
            json_offering_uuid.append(offering_uuid_item)

    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_parent_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_offering_uuid, Unset):
        json_parent_offering_uuid = str(parent_offering_uuid)
    params["parent_offering_uuid"] = json_parent_offering_uuid

    json_provider_uuid: Union[Unset, str] = UNSET
    if not isinstance(provider_uuid, Unset):
        json_provider_uuid = str(provider_uuid)
    params["provider_uuid"] = json_provider_uuid

    params["query"] = query

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["user_username"] = user_username

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-offering-users/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["OfferingUser"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OfferingUser.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OfferingUser"]]:
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
    field: Union[Unset, list[OfferingUserFieldEnum]] = UNSET,
    has_complete_profile: Union[Unset, bool] = UNSET,
    has_consent: Union[Unset, bool] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OfferingUser"]]:
    """List offering users

     Returns a paginated list of users associated with offerings. The visibility of users depends on the
    role of the authenticated user. Staff and support can see all users. Service providers can see users
    of their offerings if the user has consented. Regular users can only see their own offering-user
    records.

    Args:
        created (Union[Unset, datetime.datetime]):
        field (Union[Unset, list[OfferingUserFieldEnum]]):
        has_complete_profile (Union[Unset, bool]):
        has_consent (Union[Unset, bool]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, list[UUID]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OfferingUser']]
    """

    kwargs = _get_kwargs(
        created=created,
        field=field,
        has_complete_profile=has_complete_profile,
        has_consent=has_consent,
        is_restricted=is_restricted,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        provider_uuid=provider_uuid,
        query=query,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    field: Union[Unset, list[OfferingUserFieldEnum]] = UNSET,
    has_complete_profile: Union[Unset, bool] = UNSET,
    has_consent: Union[Unset, bool] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["OfferingUser"]:
    """List offering users

     Returns a paginated list of users associated with offerings. The visibility of users depends on the
    role of the authenticated user. Staff and support can see all users. Service providers can see users
    of their offerings if the user has consented. Regular users can only see their own offering-user
    records.

    Args:
        created (Union[Unset, datetime.datetime]):
        field (Union[Unset, list[OfferingUserFieldEnum]]):
        has_complete_profile (Union[Unset, bool]):
        has_consent (Union[Unset, bool]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, list[UUID]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingUser']
    """

    return sync_detailed(
        client=client,
        created=created,
        field=field,
        has_complete_profile=has_complete_profile,
        has_consent=has_consent,
        is_restricted=is_restricted,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        provider_uuid=provider_uuid,
        query=query,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    field: Union[Unset, list[OfferingUserFieldEnum]] = UNSET,
    has_complete_profile: Union[Unset, bool] = UNSET,
    has_consent: Union[Unset, bool] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["OfferingUser"]]:
    """List offering users

     Returns a paginated list of users associated with offerings. The visibility of users depends on the
    role of the authenticated user. Staff and support can see all users. Service providers can see users
    of their offerings if the user has consented. Regular users can only see their own offering-user
    records.

    Args:
        created (Union[Unset, datetime.datetime]):
        field (Union[Unset, list[OfferingUserFieldEnum]]):
        has_complete_profile (Union[Unset, bool]):
        has_consent (Union[Unset, bool]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, list[UUID]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OfferingUser']]
    """

    kwargs = _get_kwargs(
        created=created,
        field=field,
        has_complete_profile=has_complete_profile,
        has_consent=has_consent,
        is_restricted=is_restricted,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        parent_offering_uuid=parent_offering_uuid,
        provider_uuid=provider_uuid,
        query=query,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    field: Union[Unset, list[OfferingUserFieldEnum]] = UNSET,
    has_complete_profile: Union[Unset, bool] = UNSET,
    has_consent: Union[Unset, bool] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["OfferingUser"]:
    """List offering users

     Returns a paginated list of users associated with offerings. The visibility of users depends on the
    role of the authenticated user. Staff and support can see all users. Service providers can see users
    of their offerings if the user has consented. Regular users can only see their own offering-user
    records.

    Args:
        created (Union[Unset, datetime.datetime]):
        field (Union[Unset, list[OfferingUserFieldEnum]]):
        has_complete_profile (Union[Unset, bool]):
        has_consent (Union[Unset, bool]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, list[UUID]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_offering_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingUser']
    """

    return (
        await asyncio_detailed(
            client=client,
            created=created,
            field=field,
            has_complete_profile=has_complete_profile,
            has_consent=has_consent,
            is_restricted=is_restricted,
            modified=modified,
            o=o,
            offering=offering,
            offering_slug=offering_slug,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            parent_offering_uuid=parent_offering_uuid,
            provider_uuid=provider_uuid,
            query=query,
            state=state,
            user_username=user_username,
            user_uuid=user_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created: Union[Unset, datetime.datetime] = UNSET,
    field: Union[Unset, list[OfferingUserFieldEnum]] = UNSET,
    has_complete_profile: Union[Unset, bool] = UNSET,
    has_consent: Union[Unset, bool] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["OfferingUser"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        field (Union[Unset, list[OfferingUserFieldEnum]]):
        has_complete_profile (Union[Unset, bool]):
        has_consent (Union[Unset, bool]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, list[UUID]]):
        parent_offering_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingUser']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OfferingUser] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        field=field,
        has_complete_profile=has_complete_profile,
        has_consent=has_consent,
        is_restricted=is_restricted,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        parent_offering_uuid=parent_offering_uuid,
        provider_uuid=provider_uuid,
        query=query,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
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
    field: Union[Unset, list[OfferingUserFieldEnum]] = UNSET,
    has_complete_profile: Union[Unset, bool] = UNSET,
    has_consent: Union[Unset, bool] = UNSET,
    is_restricted: Union[Unset, bool] = UNSET,
    modified: Union[Unset, datetime.datetime] = UNSET,
    o: Union[Unset, list[OfferingUserOEnum]] = UNSET,
    offering: Union[Unset, str] = UNSET,
    offering_slug: Union[Unset, list[str]] = UNSET,
    offering_uuid: Union[Unset, list[UUID]] = UNSET,
    parent_offering_uuid: Union[Unset, UUID] = UNSET,
    provider_uuid: Union[Unset, UUID] = UNSET,
    query: Union[Unset, str] = UNSET,
    state: Union[Unset, list[OfferingUserState]] = UNSET,
    user_username: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["OfferingUser"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created (Union[Unset, datetime.datetime]):
        field (Union[Unset, list[OfferingUserFieldEnum]]):
        has_complete_profile (Union[Unset, bool]):
        has_consent (Union[Unset, bool]):
        is_restricted (Union[Unset, bool]):
        modified (Union[Unset, datetime.datetime]):
        o (Union[Unset, list[OfferingUserOEnum]]):
        offering (Union[Unset, str]):
        offering_slug (Union[Unset, list[str]]):
        offering_uuid (Union[Unset, list[UUID]]):
        parent_offering_uuid (Union[Unset, UUID]):
        provider_uuid (Union[Unset, UUID]):
        query (Union[Unset, str]):
        state (Union[Unset, list[OfferingUserState]]):
        user_username (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingUser']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OfferingUser] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created=created,
        field=field,
        has_complete_profile=has_complete_profile,
        has_consent=has_consent,
        is_restricted=is_restricted,
        modified=modified,
        o=o,
        offering=offering,
        offering_slug=offering_slug,
        offering_uuid=offering_uuid,
        parent_offering_uuid=parent_offering_uuid,
        provider_uuid=provider_uuid,
        query=query,
        state=state,
        user_username=user_username,
        user_uuid=user_uuid,
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
