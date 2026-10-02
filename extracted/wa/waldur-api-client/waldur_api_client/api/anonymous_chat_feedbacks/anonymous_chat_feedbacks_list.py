import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.anonymous_chat_feedback import AnonymousChatFeedback
from ...models.anonymous_chat_feedback_o_enum import AnonymousChatFeedbackOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    category: Union[Unset, str] = UNSET,
    has_comment: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatFeedbackOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    score: Union[Unset, int] = UNSET,
    submitted_from: Union[Unset, datetime.date] = UNSET,
    submitted_to: Union[Unset, datetime.date] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["category"] = category

    params["has_comment"] = has_comment

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["score"] = score

    json_submitted_from: Union[Unset, str] = UNSET
    if not isinstance(submitted_from, Unset):
        json_submitted_from = submitted_from.isoformat()
    params["submitted_from"] = json_submitted_from

    json_submitted_to: Union[Unset, str] = UNSET
    if not isinstance(submitted_to, Unset):
        json_submitted_to = submitted_to.isoformat()
    params["submitted_to"] = json_submitted_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/anonymous-chat-feedbacks/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["AnonymousChatFeedback"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AnonymousChatFeedback.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AnonymousChatFeedback"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    has_comment: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatFeedbackOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    score: Union[Unset, int] = UNSET,
    submitted_from: Union[Unset, datetime.date] = UNSET,
    submitted_to: Union[Unset, datetime.date] = UNSET,
) -> Response[list["AnonymousChatFeedback"]]:
    """
    Args:
        category (Union[Unset, str]):
        has_comment (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatFeedbackOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        score (Union[Unset, int]):
        submitted_from (Union[Unset, datetime.date]):
        submitted_to (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatFeedback']]
    """

    kwargs = _get_kwargs(
        category=category,
        has_comment=has_comment,
        o=o,
        page=page,
        page_size=page_size,
        score=score,
        submitted_from=submitted_from,
        submitted_to=submitted_to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    has_comment: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatFeedbackOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    score: Union[Unset, int] = UNSET,
    submitted_from: Union[Unset, datetime.date] = UNSET,
    submitted_to: Union[Unset, datetime.date] = UNSET,
) -> list["AnonymousChatFeedback"]:
    """
    Args:
        category (Union[Unset, str]):
        has_comment (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatFeedbackOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        score (Union[Unset, int]):
        submitted_from (Union[Unset, datetime.date]):
        submitted_to (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatFeedback']
    """

    return sync_detailed(
        client=client,
        category=category,
        has_comment=has_comment,
        o=o,
        page=page,
        page_size=page_size,
        score=score,
        submitted_from=submitted_from,
        submitted_to=submitted_to,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    has_comment: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatFeedbackOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    score: Union[Unset, int] = UNSET,
    submitted_from: Union[Unset, datetime.date] = UNSET,
    submitted_to: Union[Unset, datetime.date] = UNSET,
) -> Response[list["AnonymousChatFeedback"]]:
    """
    Args:
        category (Union[Unset, str]):
        has_comment (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatFeedbackOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        score (Union[Unset, int]):
        submitted_from (Union[Unset, datetime.date]):
        submitted_to (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnonymousChatFeedback']]
    """

    kwargs = _get_kwargs(
        category=category,
        has_comment=has_comment,
        o=o,
        page=page,
        page_size=page_size,
        score=score,
        submitted_from=submitted_from,
        submitted_to=submitted_to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    has_comment: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatFeedbackOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    score: Union[Unset, int] = UNSET,
    submitted_from: Union[Unset, datetime.date] = UNSET,
    submitted_to: Union[Unset, datetime.date] = UNSET,
) -> list["AnonymousChatFeedback"]:
    """
    Args:
        category (Union[Unset, str]):
        has_comment (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatFeedbackOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        score (Union[Unset, int]):
        submitted_from (Union[Unset, datetime.date]):
        submitted_to (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatFeedback']
    """

    return (
        await asyncio_detailed(
            client=client,
            category=category,
            has_comment=has_comment,
            o=o,
            page=page,
            page_size=page_size,
            score=score,
            submitted_from=submitted_from,
            submitted_to=submitted_to,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    category: Union[Unset, str] = UNSET,
    has_comment: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatFeedbackOEnum]] = UNSET,
    score: Union[Unset, int] = UNSET,
    submitted_from: Union[Unset, datetime.date] = UNSET,
    submitted_to: Union[Unset, datetime.date] = UNSET,
) -> list["AnonymousChatFeedback"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        category (Union[Unset, str]):
        has_comment (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatFeedbackOEnum]]):
        score (Union[Unset, int]):
        submitted_from (Union[Unset, datetime.date]):
        submitted_to (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatFeedback']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AnonymousChatFeedback] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        category=category,
        has_comment=has_comment,
        o=o,
        score=score,
        submitted_from=submitted_from,
        submitted_to=submitted_to,
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
    category: Union[Unset, str] = UNSET,
    has_comment: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[AnonymousChatFeedbackOEnum]] = UNSET,
    score: Union[Unset, int] = UNSET,
    submitted_from: Union[Unset, datetime.date] = UNSET,
    submitted_to: Union[Unset, datetime.date] = UNSET,
) -> list["AnonymousChatFeedback"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        category (Union[Unset, str]):
        has_comment (Union[Unset, bool]):
        o (Union[Unset, list[AnonymousChatFeedbackOEnum]]):
        score (Union[Unset, int]):
        submitted_from (Union[Unset, datetime.date]):
        submitted_to (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnonymousChatFeedback']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AnonymousChatFeedback] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        category=category,
        has_comment=has_comment,
        o=o,
        score=score,
        submitted_from=submitted_from,
        submitted_to=submitted_to,
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
