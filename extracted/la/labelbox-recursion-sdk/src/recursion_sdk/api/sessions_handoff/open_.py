from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_handoff_access_response import ManagedAgentsHandoffAccessResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/sessions/{session_id}/handoff/access".format(session_id=quote(str(session_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsHandoffAccessResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiError.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiError.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = ManagedAgentsApiError.from_dict(response.json())



        return response_409

    if response.status_code == 422:
        response_422 = ManagedAgentsApiError.from_dict(response.json())



        return response_422

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse]:
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

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse]:
    """ Open temporary access to a handed-off browser

     Atomically claims the active browser handoff for the session owner or an organization administrator,
    then returns an ephemeral redemption URL for the session's existing noVNC display. Only one user may
    drive at a time; the same user may retry safely. The URL is never persisted or logged and every
    successful response is Cache-Control: no-store. Resolve the handoff by sending one event of type
    handoff_resolved to sendSessionEvents.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse | None:
    """ Open temporary access to a handed-off browser

     Atomically claims the active browser handoff for the session owner or an organization administrator,
    then returns an ephemeral redemption URL for the session's existing noVNC display. Only one user may
    drive at a time; the same user may retry safely. The URL is never persisted or logged and every
    successful response is Cache-Control: no-store. Resolve the handoff by sending one event of type
    handoff_resolved to sendSessionEvents.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse
     """


    return sync_detailed(
        session_id=session_id,
client=client,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse]:
    """ Open temporary access to a handed-off browser

     Atomically claims the active browser handoff for the session owner or an organization administrator,
    then returns an ephemeral redemption URL for the session's existing noVNC display. Only one user may
    drive at a time; the same user may retry safely. The URL is never persisted or logged and every
    successful response is Cache-Control: no-store. Resolve the handoff by sending one event of type
    handoff_resolved to sendSessionEvents.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse | None:
    """ Open temporary access to a handed-off browser

     Atomically claims the active browser handoff for the session owner or an organization administrator,
    then returns an ephemeral redemption URL for the session's existing noVNC display. Only one user may
    drive at a time; the same user may retry safely. The URL is never persisted or logged and every
    successful response is Cache-Control: no-store. Resolve the handoff by sending one event of type
    handoff_resolved to sendSessionEvents.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsHandoffAccessResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,

    )).parsed
