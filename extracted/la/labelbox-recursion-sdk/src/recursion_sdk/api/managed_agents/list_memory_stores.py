from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_memory_stores_origin import ListMemoryStoresOrigin
from ...models.list_memory_stores_status import ListMemoryStoresStatus
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_memory_store_list_response import ManagedAgentsMemoryStoreListResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    agent_id: str | Unset = UNSET,
    origin: ListMemoryStoresOrigin | Unset = UNSET,
    status: ListMemoryStoresStatus | Unset = UNSET,
    include_archived: bool | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    json_origin: str | Unset = UNSET
    if not isinstance(origin, Unset):
        json_origin = origin.value

    params["origin"] = json_origin

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["include_archived"] = include_archived


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/memory_stores",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsMemoryStoreListResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse]:
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
    origin: ListMemoryStoresOrigin | Unset = UNSET,
    status: ListMemoryStoresStatus | Unset = UNSET,
    include_archived: bool | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse]:
    """ List memory stores

     Returns the memory stores in the calling organization, newest first. Archived stores are omitted
    unless include_archived is set. A store's contents are never disclosed in a session's prompt:
    attaching one adds a single note naming what it holds, and the agent browses, searches, and reads on
    demand, so what a session pays does not grow with what the agent has learned.

    Args:
        agent_id (str | Unset): Only stores belonging to this agent.
        origin (ListMemoryStoresOrigin | Unset): Only stores with this provenance.
        status (ListMemoryStoresStatus | Unset): Only stores in this state.
        include_archived (bool | Unset): Include archived stores. Omitted by default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
origin=origin,
status=status,
include_archived=include_archived,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    origin: ListMemoryStoresOrigin | Unset = UNSET,
    status: ListMemoryStoresStatus | Unset = UNSET,
    include_archived: bool | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse | None:
    """ List memory stores

     Returns the memory stores in the calling organization, newest first. Archived stores are omitted
    unless include_archived is set. A store's contents are never disclosed in a session's prompt:
    attaching one adds a single note naming what it holds, and the agent browses, searches, and reads on
    demand, so what a session pays does not grow with what the agent has learned.

    Args:
        agent_id (str | Unset): Only stores belonging to this agent.
        origin (ListMemoryStoresOrigin | Unset): Only stores with this provenance.
        status (ListMemoryStoresStatus | Unset): Only stores in this state.
        include_archived (bool | Unset): Include archived stores. Omitted by default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse
     """


    return sync_detailed(
        client=client,
agent_id=agent_id,
origin=origin,
status=status,
include_archived=include_archived,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    origin: ListMemoryStoresOrigin | Unset = UNSET,
    status: ListMemoryStoresStatus | Unset = UNSET,
    include_archived: bool | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse]:
    """ List memory stores

     Returns the memory stores in the calling organization, newest first. Archived stores are omitted
    unless include_archived is set. A store's contents are never disclosed in a session's prompt:
    attaching one adds a single note naming what it holds, and the agent browses, searches, and reads on
    demand, so what a session pays does not grow with what the agent has learned.

    Args:
        agent_id (str | Unset): Only stores belonging to this agent.
        origin (ListMemoryStoresOrigin | Unset): Only stores with this provenance.
        status (ListMemoryStoresStatus | Unset): Only stores in this state.
        include_archived (bool | Unset): Include archived stores. Omitted by default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
origin=origin,
status=status,
include_archived=include_archived,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    origin: ListMemoryStoresOrigin | Unset = UNSET,
    status: ListMemoryStoresStatus | Unset = UNSET,
    include_archived: bool | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse | None:
    """ List memory stores

     Returns the memory stores in the calling organization, newest first. Archived stores are omitted
    unless include_archived is set. A store's contents are never disclosed in a session's prompt:
    attaching one adds a single note naming what it holds, and the agent browses, searches, and reads on
    demand, so what a session pays does not grow with what the agent has learned.

    Args:
        agent_id (str | Unset): Only stores belonging to this agent.
        origin (ListMemoryStoresOrigin | Unset): Only stores with this provenance.
        status (ListMemoryStoresStatus | Unset): Only stores in this state.
        include_archived (bool | Unset): Include archived stores. Omitted by default.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryStoreListResponse
     """


    return (await asyncio_detailed(
        client=client,
agent_id=agent_id,
origin=origin,
status=status,
include_archived=include_archived,

    )).parsed
