from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_agent_memories_sort import ListAgentMemoriesSort
from ...models.managed_agents_agent_memories_page import ManagedAgentsAgentMemoriesPage
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    agent_id: UUID,
    *,
    query: str | Unset = UNSET,
    topic: str | Unset = UNSET,
    sort: ListAgentMemoriesSort | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["query"] = query

    params["topic"] = topic

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["cursor"] = cursor

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/agents/{agent_id}/memories".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsAgentMemoriesPage.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    topic: str | Unset = UNSET,
    sort: ListAgentMemoriesSort | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    """ Search an agent's current memories

     Lists current memories as a flat, searchable keyset page, with topics from the entire collection.
    Retired memories are available through detail and history reads.

    Args:
        agent_id (UUID): Agent whose permanent collection is being searched.
        query (str | Unset): Case-insensitive search across memory path, summary, and content.
        topic (str | Unset): Top-level collection topic returned in topics; filters an entire path
            segment.
        sort (ListAgentMemoriesSort | Unset): Sort by most recently updated (default) or
            alphabetically by path.
        cursor (str | Unset): Opaque next_cursor from the previous page with the same search
            settings.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
query=query,
topic=topic,
sort=sort,
cursor=cursor,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    topic: str | Unset = UNSET,
    sort: ListAgentMemoriesSort | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    """ Search an agent's current memories

     Lists current memories as a flat, searchable keyset page, with topics from the entire collection.
    Retired memories are available through detail and history reads.

    Args:
        agent_id (UUID): Agent whose permanent collection is being searched.
        query (str | Unset): Case-insensitive search across memory path, summary, and content.
        topic (str | Unset): Top-level collection topic returned in topics; filters an entire path
            segment.
        sort (ListAgentMemoriesSort | Unset): Sort by most recently updated (default) or
            alphabetically by path.
        cursor (str | Unset): Opaque next_cursor from the previous page with the same search
            settings.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
query=query,
topic=topic,
sort=sort,
cursor=cursor,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    topic: str | Unset = UNSET,
    sort: ListAgentMemoriesSort | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    """ Search an agent's current memories

     Lists current memories as a flat, searchable keyset page, with topics from the entire collection.
    Retired memories are available through detail and history reads.

    Args:
        agent_id (UUID): Agent whose permanent collection is being searched.
        query (str | Unset): Case-insensitive search across memory path, summary, and content.
        topic (str | Unset): Top-level collection topic returned in topics; filters an entire path
            segment.
        sort (ListAgentMemoriesSort | Unset): Sort by most recently updated (default) or
            alphabetically by path.
        cursor (str | Unset): Opaque next_cursor from the previous page with the same search
            settings.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
query=query,
topic=topic,
sort=sort,
cursor=cursor,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    topic: str | Unset = UNSET,
    sort: ListAgentMemoriesSort | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    """ Search an agent's current memories

     Lists current memories as a flat, searchable keyset page, with topics from the entire collection.
    Retired memories are available through detail and history reads.

    Args:
        agent_id (UUID): Agent whose permanent collection is being searched.
        query (str | Unset): Case-insensitive search across memory path, summary, and content.
        topic (str | Unset): Top-level collection topic returned in topics; filters an entire path
            segment.
        sort (ListAgentMemoriesSort | Unset): Sort by most recently updated (default) or
            alphabetically by path.
        cursor (str | Unset): Opaque next_cursor from the previous page with the same search
            settings.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgentMemoriesPage | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
query=query,
topic=topic,
sort=sort,
cursor=cursor,
limit=limit,

    )).parsed
