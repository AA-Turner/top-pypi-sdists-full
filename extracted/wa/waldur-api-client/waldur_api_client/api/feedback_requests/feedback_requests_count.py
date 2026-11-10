import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feedback_request_o_enum import FeedbackRequestOEnum
from ...models.feedback_state_enum import FeedbackStateEnum
from ...types import UNSET, Response, Unset


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
        "method": "head",
        "url": "/api/feedback-requests/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
