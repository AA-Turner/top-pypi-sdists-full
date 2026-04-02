from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.keycloak_user_group_membership_state import KeycloakUserGroupMembershipState
from ...models.offering_keycloak_membership import OfferingKeycloakMembership
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    email: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    last_name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[KeycloakUserGroupMembershipState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["email"] = email

    params["first_name"] = first_name

    json_group_uuid: Union[Unset, str] = UNSET
    if not isinstance(group_uuid, Unset):
        json_group_uuid = str(group_uuid)
    params["group_uuid"] = json_group_uuid

    params["last_name"] = last_name

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    json_role_uuid: Union[Unset, str] = UNSET
    if not isinstance(role_uuid, Unset):
        json_role_uuid = str(role_uuid)
    params["role_uuid"] = json_role_uuid

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/offering-keycloak-memberships/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["OfferingKeycloakMembership"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OfferingKeycloakMembership.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OfferingKeycloakMembership"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    last_name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[KeycloakUserGroupMembershipState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["OfferingKeycloakMembership"]]:
    """
    Args:
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        group_uuid (Union[Unset, UUID]):
        last_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[KeycloakUserGroupMembershipState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OfferingKeycloakMembership']]
    """

    kwargs = _get_kwargs(
        email=email,
        first_name=first_name,
        group_uuid=group_uuid,
        last_name=last_name,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
        state=state,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    last_name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[KeycloakUserGroupMembershipState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["OfferingKeycloakMembership"]:
    """
    Args:
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        group_uuid (Union[Unset, UUID]):
        last_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[KeycloakUserGroupMembershipState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingKeycloakMembership']
    """

    return sync_detailed(
        client=client,
        email=email,
        first_name=first_name,
        group_uuid=group_uuid,
        last_name=last_name,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
        state=state,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    last_name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[KeycloakUserGroupMembershipState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[list["OfferingKeycloakMembership"]]:
    """
    Args:
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        group_uuid (Union[Unset, UUID]):
        last_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[KeycloakUserGroupMembershipState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OfferingKeycloakMembership']]
    """

    kwargs = _get_kwargs(
        email=email,
        first_name=first_name,
        group_uuid=group_uuid,
        last_name=last_name,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
        state=state,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    last_name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[KeycloakUserGroupMembershipState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["OfferingKeycloakMembership"]:
    """
    Args:
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        group_uuid (Union[Unset, UUID]):
        last_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[KeycloakUserGroupMembershipState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingKeycloakMembership']
    """

    return (
        await asyncio_detailed(
            client=client,
            email=email,
            first_name=first_name,
            group_uuid=group_uuid,
            last_name=last_name,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            resource_uuid=resource_uuid,
            role_uuid=role_uuid,
            state=state,
            username=username,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    email: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    last_name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[KeycloakUserGroupMembershipState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["OfferingKeycloakMembership"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        group_uuid (Union[Unset, UUID]):
        last_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[KeycloakUserGroupMembershipState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingKeycloakMembership']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OfferingKeycloakMembership] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        email=email,
        first_name=first_name,
        group_uuid=group_uuid,
        last_name=last_name,
        offering_uuid=offering_uuid,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
        state=state,
        username=username,
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
    email: Union[Unset, str] = UNSET,
    first_name: Union[Unset, str] = UNSET,
    group_uuid: Union[Unset, UUID] = UNSET,
    last_name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[KeycloakUserGroupMembershipState]] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> list["OfferingKeycloakMembership"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        email (Union[Unset, str]):
        first_name (Union[Unset, str]):
        group_uuid (Union[Unset, UUID]):
        last_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[KeycloakUserGroupMembershipState]]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OfferingKeycloakMembership']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OfferingKeycloakMembership] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        email=email,
        first_name=first_name,
        group_uuid=group_uuid,
        last_name=last_name,
        offering_uuid=offering_uuid,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
        state=state,
        username=username,
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
