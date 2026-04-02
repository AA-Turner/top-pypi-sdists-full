from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reviewer_suggestion import ReviewerSuggestion
from ...models.reviewer_suggestion_o_enum import ReviewerSuggestionOEnum
from ...models.reviewer_suggestion_status_enum import ReviewerSuggestionStatusEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    call_uuid: Union[Unset, UUID] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[ReviewerSuggestionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[ReviewerSuggestionStatusEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    params["min_affinity_score"] = min_affinity_score

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_reviewer_uuid: Union[Unset, str] = UNSET
    if not isinstance(reviewer_uuid, Unset):
        json_reviewer_uuid = str(reviewer_uuid)
    params["reviewer_uuid"] = json_reviewer_uuid

    json_status: Union[Unset, list[str]] = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/reviewer-suggestions/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["ReviewerSuggestion"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ReviewerSuggestion.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["ReviewerSuggestion"]]:
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
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[ReviewerSuggestionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[ReviewerSuggestionStatusEnum]] = UNSET,
) -> Response[list["ReviewerSuggestion"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[ReviewerSuggestionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[ReviewerSuggestionStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ReviewerSuggestion']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        min_affinity_score=min_affinity_score,
        o=o,
        page=page,
        page_size=page_size,
        reviewer_uuid=reviewer_uuid,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[ReviewerSuggestionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[ReviewerSuggestionStatusEnum]] = UNSET,
) -> list["ReviewerSuggestion"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[ReviewerSuggestionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[ReviewerSuggestionStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ReviewerSuggestion']
    """

    return sync_detailed(
        client=client,
        call_uuid=call_uuid,
        min_affinity_score=min_affinity_score,
        o=o,
        page=page,
        page_size=page_size,
        reviewer_uuid=reviewer_uuid,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[ReviewerSuggestionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[ReviewerSuggestionStatusEnum]] = UNSET,
) -> Response[list["ReviewerSuggestion"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[ReviewerSuggestionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[ReviewerSuggestionStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['ReviewerSuggestion']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        min_affinity_score=min_affinity_score,
        o=o,
        page=page,
        page_size=page_size,
        reviewer_uuid=reviewer_uuid,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[ReviewerSuggestionOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[ReviewerSuggestionStatusEnum]] = UNSET,
) -> list["ReviewerSuggestion"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[ReviewerSuggestionOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[ReviewerSuggestionStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ReviewerSuggestion']
    """

    return (
        await asyncio_detailed(
            client=client,
            call_uuid=call_uuid,
            min_affinity_score=min_affinity_score,
            o=o,
            page=page,
            page_size=page_size,
            reviewer_uuid=reviewer_uuid,
            status=status,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[ReviewerSuggestionOEnum]] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[ReviewerSuggestionStatusEnum]] = UNSET,
) -> list["ReviewerSuggestion"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[ReviewerSuggestionOEnum]]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[ReviewerSuggestionStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ReviewerSuggestion']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ReviewerSuggestion] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        min_affinity_score=min_affinity_score,
        o=o,
        reviewer_uuid=reviewer_uuid,
        status=status,
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
    min_affinity_score: Union[Unset, float] = UNSET,
    o: Union[Unset, list[ReviewerSuggestionOEnum]] = UNSET,
    reviewer_uuid: Union[Unset, UUID] = UNSET,
    status: Union[Unset, list[ReviewerSuggestionStatusEnum]] = UNSET,
) -> list["ReviewerSuggestion"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        min_affinity_score (Union[Unset, float]):
        o (Union[Unset, list[ReviewerSuggestionOEnum]]):
        reviewer_uuid (Union[Unset, UUID]):
        status (Union[Unset, list[ReviewerSuggestionStatusEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['ReviewerSuggestion']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[ReviewerSuggestion] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        min_affinity_score=min_affinity_score,
        o=o,
        reviewer_uuid=reviewer_uuid,
        status=status,
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
