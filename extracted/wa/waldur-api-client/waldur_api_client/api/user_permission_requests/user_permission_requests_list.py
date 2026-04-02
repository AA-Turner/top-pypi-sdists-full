from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.permission_request import PermissionRequest
from ...models.proposal_review_o_enum import ProposalReviewOEnum
from ...models.remote_project_update_request_state_enum import RemoteProjectUpdateRequestStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_by: Union[Unset, str] = UNSET
    if not isinstance(created_by, Unset):
        json_created_by = str(created_by)
    params["created_by"] = json_created_by

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_invitation: Union[Unset, str] = UNSET
    if not isinstance(invitation, Unset):
        json_invitation = str(invitation)
    params["invitation"] = json_invitation

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["scope"] = scope

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
        "url": "/api/user-permission-requests/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["PermissionRequest"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PermissionRequest.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["PermissionRequest"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> Response[list["PermissionRequest"]]:
    """List permission requests

     Retrieve a list of permission requests visible to the user.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PermissionRequest']]
    """

    kwargs = _get_kwargs(
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        page=page,
        page_size=page_size,
        scope=scope,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> list["PermissionRequest"]:
    """List permission requests

     Retrieve a list of permission requests visible to the user.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PermissionRequest']
    """

    return sync_detailed(
        client=client,
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        page=page,
        page_size=page_size,
        scope=scope,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> Response[list["PermissionRequest"]]:
    """List permission requests

     Retrieve a list of permission requests visible to the user.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['PermissionRequest']]
    """

    kwargs = _get_kwargs(
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        page=page,
        page_size=page_size,
        scope=scope,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> list["PermissionRequest"]:
    """List permission requests

     Retrieve a list of permission requests visible to the user.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PermissionRequest']
    """

    return (
        await asyncio_detailed(
            client=client,
            created_by=created_by,
            customer_uuid=customer_uuid,
            invitation=invitation,
            o=o,
            page=page,
            page_size=page_size,
            scope=scope,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> list["PermissionRequest"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PermissionRequest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PermissionRequest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        scope=scope,
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
    created_by: Union[Unset, UUID] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    invitation: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[ProposalReviewOEnum]] = UNSET,
    scope: Union[Unset, str] = UNSET,
    state: Union[Unset, list[RemoteProjectUpdateRequestStateEnum]] = UNSET,
) -> list["PermissionRequest"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_by (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        invitation (Union[Unset, UUID]):
        o (Union[Unset, list[ProposalReviewOEnum]]):
        scope (Union[Unset, str]):
        state (Union[Unset, list[RemoteProjectUpdateRequestStateEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['PermissionRequest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[PermissionRequest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_by=created_by,
        customer_uuid=customer_uuid,
        invitation=invitation,
        o=o,
        scope=scope,
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
