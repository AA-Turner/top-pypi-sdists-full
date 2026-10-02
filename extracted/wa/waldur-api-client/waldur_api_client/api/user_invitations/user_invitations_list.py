from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invitation import Invitation
from ...models.invitation_o_enum import InvitationOEnum
from ...models.invitation_state import InvitationState
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    email: Union[Unset, str] = UNSET,
    email_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[InvitationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_description: Union[Unset, str] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    state: Union[Unset, list[InvitationState]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["civil_number"] = civil_number

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    params["email"] = email

    params["email_exact"] = email_exact

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["role_name"] = role_name

    json_role_uuid: Union[Unset, str] = UNSET
    if not isinstance(role_uuid, Unset):
        json_role_uuid = str(role_uuid)
    params["role_uuid"] = json_role_uuid

    params["scope"] = scope

    params["scope_description"] = scope_description

    params["scope_name"] = scope_name

    params["scope_type"] = scope_type

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
        "url": "/api/user-invitations/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["Invitation"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Invitation.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Invitation"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    email: Union[Unset, str] = UNSET,
    email_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[InvitationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_description: Union[Unset, str] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    state: Union[Unset, list[InvitationState]] = UNSET,
) -> Response[list["Invitation"]]:
    """List user invitations

     Retrieve a list of user invitations visible to the current user.

    Args:
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        email (Union[Unset, str]):
        email_exact (Union[Unset, str]):
        o (Union[Unset, list[InvitationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_description (Union[Unset, str]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        state (Union[Unset, list[InvitationState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Invitation']]
    """

    kwargs = _get_kwargs(
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        email=email,
        email_exact=email_exact,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_description=scope_description,
        scope_name=scope_name,
        scope_type=scope_type,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    email: Union[Unset, str] = UNSET,
    email_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[InvitationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_description: Union[Unset, str] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    state: Union[Unset, list[InvitationState]] = UNSET,
) -> list["Invitation"]:
    """List user invitations

     Retrieve a list of user invitations visible to the current user.

    Args:
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        email (Union[Unset, str]):
        email_exact (Union[Unset, str]):
        o (Union[Unset, list[InvitationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_description (Union[Unset, str]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        state (Union[Unset, list[InvitationState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Invitation']
    """

    return sync_detailed(
        client=client,
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        email=email,
        email_exact=email_exact,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_description=scope_description,
        scope_name=scope_name,
        scope_type=scope_type,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    email: Union[Unset, str] = UNSET,
    email_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[InvitationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_description: Union[Unset, str] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    state: Union[Unset, list[InvitationState]] = UNSET,
) -> Response[list["Invitation"]]:
    """List user invitations

     Retrieve a list of user invitations visible to the current user.

    Args:
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        email (Union[Unset, str]):
        email_exact (Union[Unset, str]):
        o (Union[Unset, list[InvitationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_description (Union[Unset, str]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        state (Union[Unset, list[InvitationState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Invitation']]
    """

    kwargs = _get_kwargs(
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        email=email,
        email_exact=email_exact,
        o=o,
        page=page,
        page_size=page_size,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_description=scope_description,
        scope_name=scope_name,
        scope_type=scope_type,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    email: Union[Unset, str] = UNSET,
    email_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[InvitationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_description: Union[Unset, str] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    state: Union[Unset, list[InvitationState]] = UNSET,
) -> list["Invitation"]:
    """List user invitations

     Retrieve a list of user invitations visible to the current user.

    Args:
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        email (Union[Unset, str]):
        email_exact (Union[Unset, str]):
        o (Union[Unset, list[InvitationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_description (Union[Unset, str]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        state (Union[Unset, list[InvitationState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Invitation']
    """

    return (
        await asyncio_detailed(
            client=client,
            civil_number=civil_number,
            customer_uuid=customer_uuid,
            email=email,
            email_exact=email_exact,
            o=o,
            page=page,
            page_size=page_size,
            role_name=role_name,
            role_uuid=role_uuid,
            scope=scope,
            scope_description=scope_description,
            scope_name=scope_name,
            scope_type=scope_type,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    email: Union[Unset, str] = UNSET,
    email_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[InvitationOEnum]] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_description: Union[Unset, str] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    state: Union[Unset, list[InvitationState]] = UNSET,
) -> list["Invitation"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        email (Union[Unset, str]):
        email_exact (Union[Unset, str]):
        o (Union[Unset, list[InvitationOEnum]]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_description (Union[Unset, str]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        state (Union[Unset, list[InvitationState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Invitation']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Invitation] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        email=email,
        email_exact=email_exact,
        o=o,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_description=scope_description,
        scope_name=scope_name,
        scope_type=scope_type,
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
    civil_number: Union[Unset, str] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    email: Union[Unset, str] = UNSET,
    email_exact: Union[Unset, str] = UNSET,
    o: Union[Unset, list[InvitationOEnum]] = UNSET,
    role_name: Union[Unset, str] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
    scope: Union[Unset, str] = UNSET,
    scope_description: Union[Unset, str] = UNSET,
    scope_name: Union[Unset, str] = UNSET,
    scope_type: Union[Unset, str] = UNSET,
    state: Union[Unset, list[InvitationState]] = UNSET,
) -> list["Invitation"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        civil_number (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        email (Union[Unset, str]):
        email_exact (Union[Unset, str]):
        o (Union[Unset, list[InvitationOEnum]]):
        role_name (Union[Unset, str]):
        role_uuid (Union[Unset, UUID]):
        scope (Union[Unset, str]):
        scope_description (Union[Unset, str]):
        scope_name (Union[Unset, str]):
        scope_type (Union[Unset, str]):
        state (Union[Unset, list[InvitationState]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Invitation']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Invitation] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        civil_number=civil_number,
        customer_uuid=customer_uuid,
        email=email,
        email_exact=email_exact,
        o=o,
        role_name=role_name,
        role_uuid=role_uuid,
        scope=scope,
        scope_description=scope_description,
        scope_name=scope_name,
        scope_type=scope_type,
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
