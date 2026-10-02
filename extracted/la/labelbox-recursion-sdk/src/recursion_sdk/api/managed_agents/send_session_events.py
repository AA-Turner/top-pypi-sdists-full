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
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_events_accepted_response import ManagedAgentsEventsAcceptedResponse
from ...models.managed_agents_session_event_send_request import ManagedAgentsSessionEventSendRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    body: ManagedAgentsSessionEventSendRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/sessions/{session_id}/events".format(session_id=quote(str(session_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEventsAcceptedResponse.from_dict(response.json())



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

    if response.status_code == 413:
        response_413 = ManagedAgentsApiError.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]:
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
    body: ManagedAgentsSessionEventSendRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]:
    """ Append user/system events to a session

     Accepts ordered user and system messages and returns how many were accepted. A running session is
    signalled so the agent wakes and sees them; once the workflow is gone the events are appended to the
    transcript instead, which the temporal_signaled field distinguishes. Events are appended in the
    order given. An omitted or empty events array yields exactly one user turn built from message; the
    request fails with 400 only when every entry sent was dropped, leaving nothing to append. A top-
    level image or document block may name a file with source {type: file, file_id}: an unknown,
    expired, or foreign file answers 404 on that block's source.file_id, a file the block cannot carry
    (a file whose bytes are not an image on an image block, a binary on a document block, a document
    over 512 KiB, more than 1 MiB of documents in one event, more than 100 such blocks, or more than 32
    MiB of catalog bytes in one request) answers 400 there, and nothing is appended to the transcript;
    copies of files resolved before the refusal stay in the session's content store, content-addressed
    and swept when unreferenced. Without file storage such a block answers 503
    file_storage_unconfigured.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsSessionEventSendRequest): Request body of POST
            /v1/sessions/{session_id}/events. It has two mutually exclusive forms and events wins:
            send message for the common case of one plain-text user turn, or send events as ordered
            typed turns with provider-shaped content. An empty events array always yields exactly one
            user turn built from message, even when message is empty. The handoff_resolved control
            form rejects all message and referenced-session fields. The response acknowledges durable
            acceptance of the turn, not the agent's reply. Example: {'actor': 'human:api', 'events':
            [{'actor': 'human:api', 'content': [{'byte_size': 1, 'content': [], 'context': 'example',
            'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True,
            'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example',
            'provider': 'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint':
            'example', 'sha256': 'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'handoff_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'note': 'example', 'text': 'example', 'type':
            'user.message'}], 'message': 'example', 'referenced_session_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]
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
    body: ManagedAgentsSessionEventSendRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse | None:
    """ Append user/system events to a session

     Accepts ordered user and system messages and returns how many were accepted. A running session is
    signalled so the agent wakes and sees them; once the workflow is gone the events are appended to the
    transcript instead, which the temporal_signaled field distinguishes. Events are appended in the
    order given. An omitted or empty events array yields exactly one user turn built from message; the
    request fails with 400 only when every entry sent was dropped, leaving nothing to append. A top-
    level image or document block may name a file with source {type: file, file_id}: an unknown,
    expired, or foreign file answers 404 on that block's source.file_id, a file the block cannot carry
    (a file whose bytes are not an image on an image block, a binary on a document block, a document
    over 512 KiB, more than 1 MiB of documents in one event, more than 100 such blocks, or more than 32
    MiB of catalog bytes in one request) answers 400 there, and nothing is appended to the transcript;
    copies of files resolved before the refusal stay in the session's content store, content-addressed
    and swept when unreferenced. Without file storage such a block answers 503
    file_storage_unconfigured.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsSessionEventSendRequest): Request body of POST
            /v1/sessions/{session_id}/events. It has two mutually exclusive forms and events wins:
            send message for the common case of one plain-text user turn, or send events as ordered
            typed turns with provider-shaped content. An empty events array always yields exactly one
            user turn built from message, even when message is empty. The handoff_resolved control
            form rejects all message and referenced-session fields. The response acknowledges durable
            acceptance of the turn, not the agent's reply. Example: {'actor': 'human:api', 'events':
            [{'actor': 'human:api', 'content': [{'byte_size': 1, 'content': [], 'context': 'example',
            'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True,
            'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example',
            'provider': 'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint':
            'example', 'sha256': 'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'handoff_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'note': 'example', 'text': 'example', 'type':
            'user.message'}], 'message': 'example', 'referenced_session_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse
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
    body: ManagedAgentsSessionEventSendRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]:
    """ Append user/system events to a session

     Accepts ordered user and system messages and returns how many were accepted. A running session is
    signalled so the agent wakes and sees them; once the workflow is gone the events are appended to the
    transcript instead, which the temporal_signaled field distinguishes. Events are appended in the
    order given. An omitted or empty events array yields exactly one user turn built from message; the
    request fails with 400 only when every entry sent was dropped, leaving nothing to append. A top-
    level image or document block may name a file with source {type: file, file_id}: an unknown,
    expired, or foreign file answers 404 on that block's source.file_id, a file the block cannot carry
    (a file whose bytes are not an image on an image block, a binary on a document block, a document
    over 512 KiB, more than 1 MiB of documents in one event, more than 100 such blocks, or more than 32
    MiB of catalog bytes in one request) answers 400 there, and nothing is appended to the transcript;
    copies of files resolved before the refusal stay in the session's content store, content-addressed
    and swept when unreferenced. Without file storage such a block answers 503
    file_storage_unconfigured.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsSessionEventSendRequest): Request body of POST
            /v1/sessions/{session_id}/events. It has two mutually exclusive forms and events wins:
            send message for the common case of one plain-text user turn, or send events as ordered
            typed turns with provider-shaped content. An empty events array always yields exactly one
            user turn built from message, even when message is empty. The handoff_resolved control
            form rejects all message and referenced-session fields. The response acknowledges durable
            acceptance of the turn, not the agent's reply. Example: {'actor': 'human:api', 'events':
            [{'actor': 'human:api', 'content': [{'byte_size': 1, 'content': [], 'context': 'example',
            'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True,
            'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example',
            'provider': 'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint':
            'example', 'sha256': 'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'handoff_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'note': 'example', 'text': 'example', 'type':
            'user.message'}], 'message': 'example', 'referenced_session_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]
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
    body: ManagedAgentsSessionEventSendRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse | None:
    """ Append user/system events to a session

     Accepts ordered user and system messages and returns how many were accepted. A running session is
    signalled so the agent wakes and sees them; once the workflow is gone the events are appended to the
    transcript instead, which the temporal_signaled field distinguishes. Events are appended in the
    order given. An omitted or empty events array yields exactly one user turn built from message; the
    request fails with 400 only when every entry sent was dropped, leaving nothing to append. A top-
    level image or document block may name a file with source {type: file, file_id}: an unknown,
    expired, or foreign file answers 404 on that block's source.file_id, a file the block cannot carry
    (a file whose bytes are not an image on an image block, a binary on a document block, a document
    over 512 KiB, more than 1 MiB of documents in one event, more than 100 such blocks, or more than 32
    MiB of catalog bytes in one request) answers 400 there, and nothing is appended to the transcript;
    copies of files resolved before the refusal stay in the session's content store, content-addressed
    and swept when unreferenced. Without file storage such a block answers 503
    file_storage_unconfigured.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsSessionEventSendRequest): Request body of POST
            /v1/sessions/{session_id}/events. It has two mutually exclusive forms and events wins:
            send message for the common case of one plain-text user turn, or send events as ordered
            typed turns with provider-shaped content. An empty events array always yields exactly one
            user turn built from message, even when message is empty. The handoff_resolved control
            form rejects all message and referenced-session fields. The response acknowledges durable
            acceptance of the turn, not the agent's reply. Example: {'actor': 'human:api', 'events':
            [{'actor': 'human:api', 'content': [{'byte_size': 1, 'content': [], 'context': 'example',
            'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True,
            'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example',
            'provider': 'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint':
            'example', 'sha256': 'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'handoff_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'note': 'example', 'text': 'example', 'type':
            'user.message'}], 'message': 'example', 'referenced_session_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,

    )).parsed
