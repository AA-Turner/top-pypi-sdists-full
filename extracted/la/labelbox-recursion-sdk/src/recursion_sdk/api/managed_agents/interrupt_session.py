from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_interrupt_request import ManagedAgentsInterruptRequest
from ...models.managed_agents_interrupted_response import ManagedAgentsInterruptedResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    body: ManagedAgentsInterruptRequest | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/sessions/{session_id}/interrupt".format(session_id=quote(str(session_id), safe=""),),
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsInterruptedResponse.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = ManagedAgentsApiError.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = ManagedAgentsApiError.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse]:
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
    body: ManagedAgentsInterruptRequest | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse]:
    """ Interrupt a running session

     Stops active model generation immediately on version-enabled workflows and gives an active tool a
    bounded grace period. A workflow history that predates immediate interruption safely retains its
    recorded bounded grace behavior. Interrupting is also how queued input is read sooner: when messages
    are waiting, the newest becomes the instruction for a fresh turn instead of leaving the session
    idle. With nothing waiting the session is left idle so a later follow-up can resume it.
    temporal_signaled reports whether a live workflow received the request; false means there was
    nothing running to interrupt. Omit message to use a default one.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptRequest | Unset): Request body for interrupting a running
            session, optionally injecting a message the agent sees at the interruption point. Example:
            {'message': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsInterruptRequest | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse | None:
    """ Interrupt a running session

     Stops active model generation immediately on version-enabled workflows and gives an active tool a
    bounded grace period. A workflow history that predates immediate interruption safely retains its
    recorded bounded grace behavior. Interrupting is also how queued input is read sooner: when messages
    are waiting, the newest becomes the instruction for a fresh turn instead of leaving the session
    idle. With nothing waiting the session is left idle so a later follow-up can resume it.
    temporal_signaled reports whether a live workflow received the request; false means there was
    nothing running to interrupt. Omit message to use a default one.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptRequest | Unset): Request body for interrupting a running
            session, optionally injecting a message the agent sees at the interruption point. Example:
            {'message': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse
     """


    return sync_detailed(
        session_id=session_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsInterruptRequest | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse]:
    """ Interrupt a running session

     Stops active model generation immediately on version-enabled workflows and gives an active tool a
    bounded grace period. A workflow history that predates immediate interruption safely retains its
    recorded bounded grace behavior. Interrupting is also how queued input is read sooner: when messages
    are waiting, the newest becomes the instruction for a fresh turn instead of leaving the session
    idle. With nothing waiting the session is left idle so a later follow-up can resume it.
    temporal_signaled reports whether a live workflow received the request; false means there was
    nothing running to interrupt. Omit message to use a default one.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptRequest | Unset): Request body for interrupting a running
            session, optionally injecting a message the agent sees at the interruption point. Example:
            {'message': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsInterruptRequest | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse | None:
    """ Interrupt a running session

     Stops active model generation immediately on version-enabled workflows and gives an active tool a
    bounded grace period. A workflow history that predates immediate interruption safely retains its
    recorded bounded grace behavior. Interrupting is also how queued input is read sooner: when messages
    are waiting, the newest becomes the instruction for a fresh turn instead of leaving the session
    idle. With nothing waiting the session is left idle so a later follow-up can resume it.
    temporal_signaled reports whether a live workflow received the request; false means there was
    nothing running to interrupt. Omit message to use a default one.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptRequest | Unset): Request body for interrupting a running
            session, optionally injecting a message the agent sees at the interruption point. Example:
            {'message': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsInterruptedResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,

    )).parsed
