from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_session_events_hydrate import ListSessionEventsHydrate
from ...models.list_session_events_image_urls import ListSessionEventsImageUrls
from ...models.list_session_events_payloads import ListSessionEventsPayloads
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_event_page_response import ManagedAgentsEventPageResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    after_event_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    hydrate: ListSessionEventsHydrate | Unset = UNSET,
    image_urls: ListSessionEventsImageUrls | Unset = UNSET,
    payloads: ListSessionEventsPayloads | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["after_event_id"] = after_event_id

    params["limit"] = limit

    json_hydrate: str | Unset = UNSET
    if not isinstance(hydrate, Unset):
        json_hydrate = hydrate.value

    params["hydrate"] = json_hydrate

    json_image_urls: str | Unset = UNSET
    if not isinstance(image_urls, Unset):
        json_image_urls = image_urls.value

    params["image_urls"] = json_image_urls

    json_payloads: str | Unset = UNSET
    if not isinstance(payloads, Unset):
        json_payloads = payloads.value

    params["payloads"] = json_payloads


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/{session_id}/events".format(session_id=quote(str(session_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEventPageResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiError.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after_event_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    hydrate: ListSessionEventsHydrate | Unset = UNSET,
    image_urls: ListSessionEventsImageUrls | Unset = UNSET,
    payloads: ListSessionEventsPayloads | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse]:
    """ Get root timeline events

     Returns one page of the root timeline's events in chronological order, plus next_page_token to
    continue from. A page can come back shorter than limit because an aggregate serialized-byte budget
    applies as well as the count, so treat an empty page with no token as the end rather than inferring
    the end from the length. Large event payloads hydrate by default; pass payloads=refs for bounded
    stubs instead.

    Args:
        session_id (UUID): Session id (UUID) whose root timeline is read.
        after_event_id (str | Unset): Exclusive continuation cursor: a lowercase canonical UUID
            event id, normally the previous page's next_page_token. Malformed values return 400.
        limit (int | Unset): Maximum event count requested. The response may contain fewer events
            when the aggregate serialized-byte budget is reached. Default: 100.
        hydrate (ListSessionEventsHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (ListSessionEventsImageUrls | Unset): Set to signed to add a short-lived url
            (and url_expires_at) to stored image blocks within the per-read signing budget. Omitted
            when signing is unavailable or the budget is exhausted; the authenticated /images proxy
            always works.
        payloads (ListSessionEventsPayloads | Unset): External event payloads hydrate by default.
            Set refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
after_event_id=after_event_id,
limit=limit,
hydrate=hydrate,
image_urls=image_urls,
payloads=payloads,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after_event_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    hydrate: ListSessionEventsHydrate | Unset = UNSET,
    image_urls: ListSessionEventsImageUrls | Unset = UNSET,
    payloads: ListSessionEventsPayloads | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse | None:
    """ Get root timeline events

     Returns one page of the root timeline's events in chronological order, plus next_page_token to
    continue from. A page can come back shorter than limit because an aggregate serialized-byte budget
    applies as well as the count, so treat an empty page with no token as the end rather than inferring
    the end from the length. Large event payloads hydrate by default; pass payloads=refs for bounded
    stubs instead.

    Args:
        session_id (UUID): Session id (UUID) whose root timeline is read.
        after_event_id (str | Unset): Exclusive continuation cursor: a lowercase canonical UUID
            event id, normally the previous page's next_page_token. Malformed values return 400.
        limit (int | Unset): Maximum event count requested. The response may contain fewer events
            when the aggregate serialized-byte budget is reached. Default: 100.
        hydrate (ListSessionEventsHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (ListSessionEventsImageUrls | Unset): Set to signed to add a short-lived url
            (and url_expires_at) to stored image blocks within the per-read signing budget. Omitted
            when signing is unavailable or the budget is exhausted; the authenticated /images proxy
            always works.
        payloads (ListSessionEventsPayloads | Unset): External event payloads hydrate by default.
            Set refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse
     """


    return sync_detailed(
        session_id=session_id,
client=client,
after_event_id=after_event_id,
limit=limit,
hydrate=hydrate,
image_urls=image_urls,
payloads=payloads,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after_event_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    hydrate: ListSessionEventsHydrate | Unset = UNSET,
    image_urls: ListSessionEventsImageUrls | Unset = UNSET,
    payloads: ListSessionEventsPayloads | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse]:
    """ Get root timeline events

     Returns one page of the root timeline's events in chronological order, plus next_page_token to
    continue from. A page can come back shorter than limit because an aggregate serialized-byte budget
    applies as well as the count, so treat an empty page with no token as the end rather than inferring
    the end from the length. Large event payloads hydrate by default; pass payloads=refs for bounded
    stubs instead.

    Args:
        session_id (UUID): Session id (UUID) whose root timeline is read.
        after_event_id (str | Unset): Exclusive continuation cursor: a lowercase canonical UUID
            event id, normally the previous page's next_page_token. Malformed values return 400.
        limit (int | Unset): Maximum event count requested. The response may contain fewer events
            when the aggregate serialized-byte budget is reached. Default: 100.
        hydrate (ListSessionEventsHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (ListSessionEventsImageUrls | Unset): Set to signed to add a short-lived url
            (and url_expires_at) to stored image blocks within the per-read signing budget. Omitted
            when signing is unavailable or the budget is exhausted; the authenticated /images proxy
            always works.
        payloads (ListSessionEventsPayloads | Unset): External event payloads hydrate by default.
            Set refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
after_event_id=after_event_id,
limit=limit,
hydrate=hydrate,
image_urls=image_urls,
payloads=payloads,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after_event_id: str | Unset = UNSET,
    limit: int | Unset = 100,
    hydrate: ListSessionEventsHydrate | Unset = UNSET,
    image_urls: ListSessionEventsImageUrls | Unset = UNSET,
    payloads: ListSessionEventsPayloads | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse | None:
    """ Get root timeline events

     Returns one page of the root timeline's events in chronological order, plus next_page_token to
    continue from. A page can come back shorter than limit because an aggregate serialized-byte budget
    applies as well as the count, so treat an empty page with no token as the end rather than inferring
    the end from the length. Large event payloads hydrate by default; pass payloads=refs for bounded
    stubs instead.

    Args:
        session_id (UUID): Session id (UUID) whose root timeline is read.
        after_event_id (str | Unset): Exclusive continuation cursor: a lowercase canonical UUID
            event id, normally the previous page's next_page_token. Malformed values return 400.
        limit (int | Unset): Maximum event count requested. The response may contain fewer events
            when the aggregate serialized-byte budget is reached. Default: 100.
        hydrate (ListSessionEventsHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (ListSessionEventsImageUrls | Unset): Set to signed to add a short-lived url
            (and url_expires_at) to stored image blocks within the per-read signing budget. Omitted
            when signing is unavailable or the budget is exhausted; the authenticated /images proxy
            always works.
        payloads (ListSessionEventsPayloads | Unset): External event payloads hydrate by default.
            Set refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEventPageResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
after_event_id=after_event_id,
limit=limit,
hydrate=hydrate,
image_urls=image_urls,
payloads=payloads,

    )).parsed
