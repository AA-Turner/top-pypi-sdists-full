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
from ...models.managed_agents_session_thread import ManagedAgentsSessionThread
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    thread_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/{session_id}/threads/{thread_id}".format(session_id=quote(str(session_id), safe=""),thread_id=quote(str(thread_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionThread.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread]:
    """ Get session thread

     Returns one thread from the session's tree. The thread must belong to the tree rooted at the session
    in the path; anything else is a 404 rather than a cross-tree read.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        thread_id (str): Thread id as returned by listSessionThreads. Threads the runtime creates
            carry the sub-session's UUID; an imported transcript may carry the source system's own
            thread id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
thread_id=thread_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread | None:
    """ Get session thread

     Returns one thread from the session's tree. The thread must belong to the tree rooted at the session
    in the path; anything else is a 404 rather than a cross-tree read.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        thread_id (str): Thread id as returned by listSessionThreads. Threads the runtime creates
            carry the sub-session's UUID; an imported transcript may carry the source system's own
            thread id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread
     """


    return sync_detailed(
        session_id=session_id,
thread_id=thread_id,
client=client,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread]:
    """ Get session thread

     Returns one thread from the session's tree. The thread must belong to the tree rooted at the session
    in the path; anything else is a 404 rather than a cross-tree read.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        thread_id (str): Thread id as returned by listSessionThreads. Threads the runtime creates
            carry the sub-session's UUID; an imported transcript may carry the source system's own
            thread id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
thread_id=thread_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    thread_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread | None:
    """ Get session thread

     Returns one thread from the session's tree. The thread must belong to the tree rooted at the session
    in the path; anything else is a 404 rather than a cross-tree read.

    Args:
        session_id (UUID): Any session id (UUID) in the tree; the read resolves to its root
            session.
        thread_id (str): Thread id as returned by listSessionThreads. Threads the runtime creates
            carry the sub-session's UUID; an imported transcript may carry the source system's own
            thread id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionThread
     """


    return (await asyncio_detailed(
        session_id=session_id,
thread_id=thread_id,
client=client,

    )).parsed
