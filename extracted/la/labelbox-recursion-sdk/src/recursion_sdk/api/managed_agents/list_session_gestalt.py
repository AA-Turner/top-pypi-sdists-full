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
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_session_gestalt_response import ManagedAgentsSessionGestaltResponse
from ...types import UNSET, Unset
from typing import cast
import datetime



def _get_kwargs(
    *,
    agent_id: str | Unset = UNSET,
    since: datetime.datetime,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    json_since = since.isoformat()
    params["since"] = json_since


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/gestalt",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionGestaltResponse.from_dict(response.json())



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
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    since: datetime.datetime,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse]:
    """ Snapshot every root session created in a window

     Returns a compact projection of every live root session the caller may see that was created at or
    after since (at most 30 days ago), newest first, read at one instant. Rows carry only identity,
    agent, state, and timestamps; the response is meant to be drawn whole -- one tile per session -- and
    then kept current with streamSessionGestalt from as_of, not re-read. Served from a covering index,
    so its latency is a range scan of the window. Windows with more than 5000 roots are truncated to the
    newest 5000 and say so.

    Args:
        agent_id (str | Unset): Limit the snapshot to one agent in the caller workspace, before
            truncation.
        since (datetime.datetime): RFC 3339 start of the window; sessions created at or after it
            are included. At most 30 days ago globally, or 400 days with agent_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
since=since,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    since: datetime.datetime,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse | None:
    """ Snapshot every root session created in a window

     Returns a compact projection of every live root session the caller may see that was created at or
    after since (at most 30 days ago), newest first, read at one instant. Rows carry only identity,
    agent, state, and timestamps; the response is meant to be drawn whole -- one tile per session -- and
    then kept current with streamSessionGestalt from as_of, not re-read. Served from a covering index,
    so its latency is a range scan of the window. Windows with more than 5000 roots are truncated to the
    newest 5000 and say so.

    Args:
        agent_id (str | Unset): Limit the snapshot to one agent in the caller workspace, before
            truncation.
        since (datetime.datetime): RFC 3339 start of the window; sessions created at or after it
            are included. At most 30 days ago globally, or 400 days with agent_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse
     """


    return sync_detailed(
        client=client,
agent_id=agent_id,
since=since,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    since: datetime.datetime,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse]:
    """ Snapshot every root session created in a window

     Returns a compact projection of every live root session the caller may see that was created at or
    after since (at most 30 days ago), newest first, read at one instant. Rows carry only identity,
    agent, state, and timestamps; the response is meant to be drawn whole -- one tile per session -- and
    then kept current with streamSessionGestalt from as_of, not re-read. Served from a covering index,
    so its latency is a range scan of the window. Windows with more than 5000 roots are truncated to the
    newest 5000 and say so.

    Args:
        agent_id (str | Unset): Limit the snapshot to one agent in the caller workspace, before
            truncation.
        since (datetime.datetime): RFC 3339 start of the window; sessions created at or after it
            are included. At most 30 days ago globally, or 400 days with agent_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
since=since,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    since: datetime.datetime,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse | None:
    """ Snapshot every root session created in a window

     Returns a compact projection of every live root session the caller may see that was created at or
    after since (at most 30 days ago), newest first, read at one instant. Rows carry only identity,
    agent, state, and timestamps; the response is meant to be drawn whole -- one tile per session -- and
    then kept current with streamSessionGestalt from as_of, not re-read. Served from a covering index,
    so its latency is a range scan of the window. Windows with more than 5000 roots are truncated to the
    newest 5000 and say so.

    Args:
        agent_id (str | Unset): Limit the snapshot to one agent in the caller workspace, before
            truncation.
        since (datetime.datetime): RFC 3339 start of the window; sessions created at or after it
            are included. At most 30 days ago globally, or 400 days with agent_id.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsSessionGestaltResponse
     """


    return (await asyncio_detailed(
        client=client,
agent_id=agent_id,
since=since,

    )).parsed
