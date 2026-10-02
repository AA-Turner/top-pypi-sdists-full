from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_session_view import GetSessionView
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_session import ManagedAgentsSession
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    view: GetSessionView | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_view: str | Unset = UNSET
    if not isinstance(view, Unset):
        json_view = view.value

    params["view"] = json_view


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/{session_id}".format(session_id=quote(str(session_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSession.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession]:
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
    view: GetSessionView | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession]:
    """ Get session

     Returns one session with its status, agent and environment binding, and timing. Statuses completed,
    failed, and cancelled are terminal and will not change again, which is what a poller should wait
    for. Poll with view=summary once the start-time snapshots are held.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        view (GetSessionView | Unset): full (default) returns the whole session. summary omits
            agent_snapshot, model_snapshot and config — written once at start and never changed —
            which a poller that already holds them should ask for: they are most of the row's bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
view=view,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    view: GetSessionView | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession | None:
    """ Get session

     Returns one session with its status, agent and environment binding, and timing. Statuses completed,
    failed, and cancelled are terminal and will not change again, which is what a poller should wait
    for. Poll with view=summary once the start-time snapshots are held.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        view (GetSessionView | Unset): full (default) returns the whole session. summary omits
            agent_snapshot, model_snapshot and config — written once at start and never changed —
            which a poller that already holds them should ask for: they are most of the row's bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession
     """


    return sync_detailed(
        session_id=session_id,
client=client,
view=view,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    view: GetSessionView | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession]:
    """ Get session

     Returns one session with its status, agent and environment binding, and timing. Statuses completed,
    failed, and cancelled are terminal and will not change again, which is what a poller should wait
    for. Poll with view=summary once the start-time snapshots are held.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        view (GetSessionView | Unset): full (default) returns the whole session. summary omits
            agent_snapshot, model_snapshot and config — written once at start and never changed —
            which a poller that already holds them should ask for: they are most of the row's bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
view=view,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    view: GetSessionView | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession | None:
    """ Get session

     Returns one session with its status, agent and environment binding, and timing. Statuses completed,
    failed, and cancelled are terminal and will not change again, which is what a poller should wait
    for. Poll with view=summary once the start-time snapshots are held.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        view (GetSessionView | Unset): full (default) returns the whole session. summary omits
            agent_snapshot, model_snapshot and config — written once at start and never changed —
            which a poller that already holds them should ask for: they are most of the row's bytes.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSession
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
view=view,

    )).parsed
