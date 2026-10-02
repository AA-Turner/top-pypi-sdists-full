from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_session_tree_hydrate import GetSessionTreeHydrate
from ...models.get_session_tree_image_urls import GetSessionTreeImageUrls
from ...models.get_session_tree_payloads import GetSessionTreePayloads
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_tree_result import ManagedAgentsTreeResult
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    hydrate: GetSessionTreeHydrate | Unset = UNSET,
    image_urls: GetSessionTreeImageUrls | Unset = UNSET,
    payloads: GetSessionTreePayloads | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

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
        "url": "/managed-agents/v1/sessions/{session_id}/tree".format(session_id=quote(str(session_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsTreeResult.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult]:
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
    hydrate: GetSessionTreeHydrate | Unset = UNSET,
    image_urls: GetSessionTreeImageUrls | Unset = UNSET,
    payloads: GetSessionTreePayloads | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult]:
    """ Get root session tree and timeline

     Returns every session in the root session's tree, its threads, and the first bounded page of the
    merged chronological event log. When next_event_id is set, more events remain and should be fetched
    with listSessionEvents rather than by re-reading the tree. Any session id in the tree is accepted;
    the read resolves to its root.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        hydrate (GetSessionTreeHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (GetSessionTreeImageUrls | Unset): Set to signed to add a short-lived url (and
            url_expires_at) to stored image blocks within the per-read signing budget. Omitted when
            signing is unavailable or the budget is exhausted; the authenticated /images proxy always
            works.
        payloads (GetSessionTreePayloads | Unset): External event payloads hydrate by default. Set
            refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
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
    hydrate: GetSessionTreeHydrate | Unset = UNSET,
    image_urls: GetSessionTreeImageUrls | Unset = UNSET,
    payloads: GetSessionTreePayloads | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult | None:
    """ Get root session tree and timeline

     Returns every session in the root session's tree, its threads, and the first bounded page of the
    merged chronological event log. When next_event_id is set, more events remain and should be fetched
    with listSessionEvents rather than by re-reading the tree. Any session id in the tree is accepted;
    the read resolves to its root.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        hydrate (GetSessionTreeHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (GetSessionTreeImageUrls | Unset): Set to signed to add a short-lived url (and
            url_expires_at) to stored image blocks within the per-read signing budget. Omitted when
            signing is unavailable or the budget is exhausted; the authenticated /images proxy always
            works.
        payloads (GetSessionTreePayloads | Unset): External event payloads hydrate by default. Set
            refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult
     """


    return sync_detailed(
        session_id=session_id,
client=client,
hydrate=hydrate,
image_urls=image_urls,
payloads=payloads,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    hydrate: GetSessionTreeHydrate | Unset = UNSET,
    image_urls: GetSessionTreeImageUrls | Unset = UNSET,
    payloads: GetSessionTreePayloads | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult]:
    """ Get root session tree and timeline

     Returns every session in the root session's tree, its threads, and the first bounded page of the
    merged chronological event log. When next_event_id is set, more events remain and should be fetched
    with listSessionEvents rather than by re-reading the tree. Any session id in the tree is accepted;
    the read resolves to its root.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        hydrate (GetSessionTreeHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (GetSessionTreeImageUrls | Unset): Set to signed to add a short-lived url (and
            url_expires_at) to stored image blocks within the per-read signing budget. Omitted when
            signing is unavailable or the budget is exhausted; the authenticated /images proxy always
            works.
        payloads (GetSessionTreePayloads | Unset): External event payloads hydrate by default. Set
            refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
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
    hydrate: GetSessionTreeHydrate | Unset = UNSET,
    image_urls: GetSessionTreeImageUrls | Unset = UNSET,
    payloads: GetSessionTreePayloads | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult | None:
    """ Get root session tree and timeline

     Returns every session in the root session's tree, its threads, and the first bounded page of the
    merged chronological event log. When next_event_id is set, more events remain and should be fetched
    with listSessionEvents rather than by re-reading the tree. Any session id in the tree is accepted;
    the read resolves to its root.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        hydrate (GetSessionTreeHydrate | Unset): Opt-in compatibility mode. images rehydrates
            private image refs under strict response caps; omitted by default.
        image_urls (GetSessionTreeImageUrls | Unset): Set to signed to add a short-lived url (and
            url_expires_at) to stored image blocks within the per-read signing budget. Omitted when
            signing is unavailable or the budget is exhausted; the authenticated /images proxy always
            works.
        payloads (GetSessionTreePayloads | Unset): External event payloads hydrate by default. Set
            refs to return bounded stubs and private reference metadata only.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsTreeResult
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
hydrate=hydrate,
image_urls=image_urls,
payloads=payloads,

    )).parsed
