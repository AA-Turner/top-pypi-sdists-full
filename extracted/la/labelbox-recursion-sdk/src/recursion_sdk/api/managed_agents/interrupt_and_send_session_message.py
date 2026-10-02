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
from ...models.managed_agents_events_accepted_response import ManagedAgentsEventsAcceptedResponse
from ...models.managed_agents_interrupt_and_send_request import ManagedAgentsInterruptAndSendRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    body: ManagedAgentsInterruptAndSendRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/sessions/{session_id}/interrupt-and-send".format(session_id=quote(str(session_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse | None:
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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]:
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
    body: ManagedAgentsInterruptAndSendRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]:
    """ Interrupt a session and send a replacement instruction

     Stops active work and durably accepts a replacement instruction in one ordered operation. A version-
    enabled workflow starts a fresh turn automatically. A workflow history that predates redirect
    support still honors the interrupt and leaves the replacement durable for its next resume.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptAndSendRequest): Request body for interrupting the active
            operation and starting a fresh turn with one replacement instruction. Example: {'content':
            [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example',
            'encrypted_content': 'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'input': {'key': 'example'}, 'is_error': True, 'media_type': 'example', 'name': 'example-
            name', 'omitted_bytes': 1, 'payload': 'example', 'provider': 'example',
            'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256':
            'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'message': 'example', 'referenced_session_ids':
            ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]
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
    body: ManagedAgentsInterruptAndSendRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse | None:
    """ Interrupt a session and send a replacement instruction

     Stops active work and durably accepts a replacement instruction in one ordered operation. A version-
    enabled workflow starts a fresh turn automatically. A workflow history that predates redirect
    support still honors the interrupt and leaves the replacement durable for its next resume.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptAndSendRequest): Request body for interrupting the active
            operation and starting a fresh turn with one replacement instruction. Example: {'content':
            [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example',
            'encrypted_content': 'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'input': {'key': 'example'}, 'is_error': True, 'media_type': 'example', 'name': 'example-
            name', 'omitted_bytes': 1, 'payload': 'example', 'provider': 'example',
            'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256':
            'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'message': 'example', 'referenced_session_ids':
            ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse
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
    body: ManagedAgentsInterruptAndSendRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]:
    """ Interrupt a session and send a replacement instruction

     Stops active work and durably accepts a replacement instruction in one ordered operation. A version-
    enabled workflow starts a fresh turn automatically. A workflow history that predates redirect
    support still honors the interrupt and leaves the replacement durable for its next resume.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptAndSendRequest): Request body for interrupting the active
            operation and starting a fresh turn with one replacement instruction. Example: {'content':
            [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example',
            'encrypted_content': 'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'input': {'key': 'example'}, 'is_error': True, 'media_type': 'example', 'name': 'example-
            name', 'omitted_bytes': 1, 'payload': 'example', 'provider': 'example',
            'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256':
            'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'message': 'example', 'referenced_session_ids':
            ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse]
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
    body: ManagedAgentsInterruptAndSendRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse | None:
    """ Interrupt a session and send a replacement instruction

     Stops active work and durably accepts a replacement instruction in one ordered operation. A version-
    enabled workflow starts a fresh turn automatically. A workflow history that predates redirect
    support still honors the interrupt and leaves the replacement durable for its next resume.

    Args:
        session_id (UUID): Session id (UUID) as returned by startSession or listSessions.
        body (ManagedAgentsInterruptAndSendRequest): Request body for interrupting the active
            operation and starting a fresh turn with one replacement instruction. Example: {'content':
            [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example',
            'encrypted_content': 'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
            'input': {'key': 'example'}, 'is_error': True, 'media_type': 'example', 'name': 'example-
            name', 'omitted_bytes': 1, 'payload': 'example', 'provider': 'example',
            'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256':
            'example', 'signature': 'example', 'source': {'file_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example',
            'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type':
            'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at':
            '2026-02-18T09:30:00Z', 'width': 1}], 'message': 'example', 'referenced_session_ids':
            ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsEventsAcceptedResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,

    )).parsed
