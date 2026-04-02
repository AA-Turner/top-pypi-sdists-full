from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.proposal import Proposal
from ...models.proposal_o_enum import ProposalOEnum
from ...models.proposal_states import ProposalStates
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    json_created_by_uuid: Union[Unset, str] = UNSET
    if not isinstance(created_by_uuid, Unset):
        json_created_by_uuid = str(created_by_uuid)
    params["created_by_uuid"] = json_created_by_uuid

    params["my_proposals"] = my_proposals

    params["name"] = name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_organization_uuid: Union[Unset, str] = UNSET
    if not isinstance(organization_uuid, Unset):
        json_organization_uuid = str(organization_uuid)
    params["organization_uuid"] = json_organization_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_round_: Union[Unset, str] = UNSET
    if not isinstance(round_, Unset):
        json_round_ = str(round_)
    params["round"] = json_round_

    json_round_uuid: Union[Unset, str] = UNSET
    if not isinstance(round_uuid, Unset):
        json_round_uuid = str(round_uuid)
    params["round_uuid"] = json_round_uuid

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
        "url": "/api/proposal-proposals/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["Proposal"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Proposal.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Proposal"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
) -> Response[list["Proposal"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ProposalStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Proposal']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        round_=round_,
        round_uuid=round_uuid,
        state=state,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
) -> list["Proposal"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ProposalStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Proposal']
    """

    return sync_detailed(
        client=client,
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        round_=round_,
        round_uuid=round_uuid,
        state=state,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
) -> Response[list["Proposal"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ProposalStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Proposal']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        page=page,
        page_size=page_size,
        round_=round_,
        round_uuid=round_uuid,
        state=state,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
) -> list["Proposal"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ProposalStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Proposal']
    """

    return (
        await asyncio_detailed(
            client=client,
            call_uuid=call_uuid,
            created_by_uuid=created_by_uuid,
            my_proposals=my_proposals,
            name=name,
            o=o,
            organization_uuid=organization_uuid,
            page=page,
            page_size=page_size,
            round_=round_,
            round_uuid=round_uuid,
            state=state,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
) -> list["Proposal"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ProposalStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Proposal']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Proposal] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        round_=round_,
        round_uuid=round_uuid,
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
    call_uuid: Union[Unset, UUID] = UNSET,
    created_by_uuid: Union[Unset, UUID] = UNSET,
    my_proposals: Union[Unset, bool] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ProposalOEnum]] = UNSET,
    organization_uuid: Union[Unset, UUID] = UNSET,
    round_: Union[Unset, UUID] = UNSET,
    round_uuid: Union[Unset, UUID] = UNSET,
    state: Union[Unset, list[ProposalStates]] = UNSET,
) -> list["Proposal"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        created_by_uuid (Union[Unset, UUID]):
        my_proposals (Union[Unset, bool]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ProposalOEnum]]):
        organization_uuid (Union[Unset, UUID]):
        round_ (Union[Unset, UUID]):
        round_uuid (Union[Unset, UUID]):
        state (Union[Unset, list[ProposalStates]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Proposal']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Proposal] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        created_by_uuid=created_by_uuid,
        my_proposals=my_proposals,
        name=name,
        o=o,
        organization_uuid=organization_uuid,
        round_=round_,
        round_uuid=round_uuid,
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
