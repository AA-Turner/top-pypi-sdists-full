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
from ...models.managed_agents_open_session_analyst_request import ManagedAgentsOpenSessionAnalystRequest
from ...models.managed_agents_session_analyst_response import ManagedAgentsSessionAnalystResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    body: ManagedAgentsOpenSessionAnalystRequest | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/sessions/{session_id}/analyst".format(session_id=quote(str(session_id), safe=""),),
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionAnalystResponse.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = ManagedAgentsSessionAnalystResponse.from_dict(response.json())



        return response_201

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse]:
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
    body: ManagedAgentsOpenSessionAnalystRequest | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse]:
    """ Open the session analyst for a session

     Returns the caller's session analyst for the tree containing this session, starting one if they have
    none (201 when this call started it, 200 otherwise): a read-only assistant session that answers
    questions about the target -- what the agents were asked to do, what they did, which tools failed,
    how they coordinated, what it cost and how it was graded. Ask it questions by sending messages to
    the returned analyst session (sendSessionEvents) and read its answers from that session's events or
    event stream. One analyst per caller per tree: opening again returns the same conversation, and a
    body of {"reset": true} ends it; the next question starts a new one. The analyst runs on a fixed
    platform model with no sandbox and no credentials, and nothing it does changes the target session.
    Any session id in the tree is accepted; the analyst always reads the whole tree.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsOpenSessionAnalystRequest | Unset): Optional request body of
            openSessionAnalyst. An empty body returns the caller's conversation with the tree, if any;
            question asks (starting the conversation if needed); reset ends the current conversation.
            Example: {'question': 'example', 'reset': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse]
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
    body: ManagedAgentsOpenSessionAnalystRequest | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse | None:
    """ Open the session analyst for a session

     Returns the caller's session analyst for the tree containing this session, starting one if they have
    none (201 when this call started it, 200 otherwise): a read-only assistant session that answers
    questions about the target -- what the agents were asked to do, what they did, which tools failed,
    how they coordinated, what it cost and how it was graded. Ask it questions by sending messages to
    the returned analyst session (sendSessionEvents) and read its answers from that session's events or
    event stream. One analyst per caller per tree: opening again returns the same conversation, and a
    body of {"reset": true} ends it; the next question starts a new one. The analyst runs on a fixed
    platform model with no sandbox and no credentials, and nothing it does changes the target session.
    Any session id in the tree is accepted; the analyst always reads the whole tree.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsOpenSessionAnalystRequest | Unset): Optional request body of
            openSessionAnalyst. An empty body returns the caller's conversation with the tree, if any;
            question asks (starting the conversation if needed); reset ends the current conversation.
            Example: {'question': 'example', 'reset': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse
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
    body: ManagedAgentsOpenSessionAnalystRequest | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse]:
    """ Open the session analyst for a session

     Returns the caller's session analyst for the tree containing this session, starting one if they have
    none (201 when this call started it, 200 otherwise): a read-only assistant session that answers
    questions about the target -- what the agents were asked to do, what they did, which tools failed,
    how they coordinated, what it cost and how it was graded. Ask it questions by sending messages to
    the returned analyst session (sendSessionEvents) and read its answers from that session's events or
    event stream. One analyst per caller per tree: opening again returns the same conversation, and a
    body of {"reset": true} ends it; the next question starts a new one. The analyst runs on a fixed
    platform model with no sandbox and no credentials, and nothing it does changes the target session.
    Any session id in the tree is accepted; the analyst always reads the whole tree.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsOpenSessionAnalystRequest | Unset): Optional request body of
            openSessionAnalyst. An empty body returns the caller's conversation with the tree, if any;
            question asks (starting the conversation if needed); reset ends the current conversation.
            Example: {'question': 'example', 'reset': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse]
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
    body: ManagedAgentsOpenSessionAnalystRequest | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse | None:
    """ Open the session analyst for a session

     Returns the caller's session analyst for the tree containing this session, starting one if they have
    none (201 when this call started it, 200 otherwise): a read-only assistant session that answers
    questions about the target -- what the agents were asked to do, what they did, which tools failed,
    how they coordinated, what it cost and how it was graded. Ask it questions by sending messages to
    the returned analyst session (sendSessionEvents) and read its answers from that session's events or
    event stream. One analyst per caller per tree: opening again returns the same conversation, and a
    body of {"reset": true} ends it; the next question starts a new one. The analyst runs on a fixed
    platform model with no sandbox and no credentials, and nothing it does changes the target session.
    Any session id in the tree is accepted; the analyst always reads the whole tree.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsOpenSessionAnalystRequest | Unset): Optional request body of
            openSessionAnalyst. An empty body returns the caller's conversation with the tree, if any;
            question asks (starting the conversation if needed); reset ends the current conversation.
            Example: {'question': 'example', 'reset': True}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsSessionAnalystResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,

    )).parsed
