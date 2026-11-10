import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feedback_request import FeedbackRequest
from ...models.feedback_request_o_enum import FeedbackRequestOEnum
from ...models.feedback_state_enum import FeedbackStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    answered_after: Union[Unset, datetime.date] = UNSET,
    answered_before: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[FeedbackRequestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[FeedbackStateEnum]] = UNSET,
    survey_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_answered_after: Union[Unset, str] = UNSET
    if not isinstance(answered_after, Unset):
        json_answered_after = answered_after.isoformat()
    params["answered_after"] = json_answered_after

    json_answered_before: Union[Unset, str] = UNSET
    if not isinstance(answered_before, Unset):
        json_answered_before = answered_before.isoformat()
    params["answered_before"] = json_answered_before

    json_customer_uuid: Union[Unset, str] = UNSET
    if not isinstance(customer_uuid, Unset):
        json_customer_uuid = str(customer_uuid)
    params["customer_uuid"] = json_customer_uuid

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_state: Union[Unset, list[str]] = UNSET
    if not isinstance(state, Unset):
        json_state = []
        for state_item_data in state:
            state_item = state_item_data.value
            json_state.append(state_item)

    params["state"] = json_state

    json_survey_uuid: Union[Unset, str] = UNSET
    if not isinstance(survey_uuid, Unset):
        json_survey_uuid = str(survey_uuid)
    params["survey_uuid"] = json_survey_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/feedback-requests/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["FeedbackRequest"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FeedbackRequest.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["FeedbackRequest"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    answered_after: Union[Unset, datetime.date] = UNSET,
    answered_before: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[FeedbackRequestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[FeedbackStateEnum]] = UNSET,
    survey_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["FeedbackRequest"]]:
    """
    Args:
        answered_after (Union[Unset, datetime.date]):
        answered_before (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[FeedbackRequestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[FeedbackStateEnum]]):
        survey_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['FeedbackRequest']]
    """

    kwargs = _get_kwargs(
        answered_after=answered_after,
        answered_before=answered_before,
        customer_uuid=customer_uuid,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
        survey_uuid=survey_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    answered_after: Union[Unset, datetime.date] = UNSET,
    answered_before: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[FeedbackRequestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[FeedbackStateEnum]] = UNSET,
    survey_uuid: Union[Unset, UUID] = UNSET,
) -> list["FeedbackRequest"]:
    """
    Args:
        answered_after (Union[Unset, datetime.date]):
        answered_before (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[FeedbackRequestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[FeedbackStateEnum]]):
        survey_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FeedbackRequest']
    """

    return sync_detailed(
        client=client,
        answered_after=answered_after,
        answered_before=answered_before,
        customer_uuid=customer_uuid,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
        survey_uuid=survey_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    answered_after: Union[Unset, datetime.date] = UNSET,
    answered_before: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[FeedbackRequestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[FeedbackStateEnum]] = UNSET,
    survey_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["FeedbackRequest"]]:
    """
    Args:
        answered_after (Union[Unset, datetime.date]):
        answered_before (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[FeedbackRequestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[FeedbackStateEnum]]):
        survey_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['FeedbackRequest']]
    """

    kwargs = _get_kwargs(
        answered_after=answered_after,
        answered_before=answered_before,
        customer_uuid=customer_uuid,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
        survey_uuid=survey_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    answered_after: Union[Unset, datetime.date] = UNSET,
    answered_before: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[FeedbackRequestOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, list[FeedbackStateEnum]] = UNSET,
    survey_uuid: Union[Unset, UUID] = UNSET,
) -> list["FeedbackRequest"]:
    """
    Args:
        answered_after (Union[Unset, datetime.date]):
        answered_before (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[FeedbackRequestOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, list[FeedbackStateEnum]]):
        survey_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FeedbackRequest']
    """

    return (
        await asyncio_detailed(
            client=client,
            answered_after=answered_after,
            answered_before=answered_before,
            customer_uuid=customer_uuid,
            o=o,
            page=page,
            page_size=page_size,
            state=state,
            survey_uuid=survey_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    answered_after: Union[Unset, datetime.date] = UNSET,
    answered_before: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[FeedbackRequestOEnum]] = UNSET,
    state: Union[Unset, list[FeedbackStateEnum]] = UNSET,
    survey_uuid: Union[Unset, UUID] = UNSET,
) -> list["FeedbackRequest"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        answered_after (Union[Unset, datetime.date]):
        answered_before (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[FeedbackRequestOEnum]]):
        state (Union[Unset, list[FeedbackStateEnum]]):
        survey_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FeedbackRequest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[FeedbackRequest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        answered_after=answered_after,
        answered_before=answered_before,
        customer_uuid=customer_uuid,
        o=o,
        state=state,
        survey_uuid=survey_uuid,
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
    answered_after: Union[Unset, datetime.date] = UNSET,
    answered_before: Union[Unset, datetime.date] = UNSET,
    customer_uuid: Union[Unset, UUID] = UNSET,
    o: Union[Unset, list[FeedbackRequestOEnum]] = UNSET,
    state: Union[Unset, list[FeedbackStateEnum]] = UNSET,
    survey_uuid: Union[Unset, UUID] = UNSET,
) -> list["FeedbackRequest"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        answered_after (Union[Unset, datetime.date]):
        answered_before (Union[Unset, datetime.date]):
        customer_uuid (Union[Unset, UUID]):
        o (Union[Unset, list[FeedbackRequestOEnum]]):
        state (Union[Unset, list[FeedbackStateEnum]]):
        survey_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FeedbackRequest']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[FeedbackRequest] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        answered_after=answered_after,
        answered_before=answered_before,
        customer_uuid=customer_uuid,
        o=o,
        state=state,
        survey_uuid=survey_uuid,
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
