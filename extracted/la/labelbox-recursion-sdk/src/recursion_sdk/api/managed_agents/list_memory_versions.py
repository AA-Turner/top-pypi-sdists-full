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
from ...models.managed_agents_memory_version_page import ManagedAgentsMemoryVersionPage
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    memory_store_id: UUID,
    *,
    memory_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["memory_id"] = memory_id

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/memory_stores/{memory_store_id}/memory_versions".format(memory_store_id=quote(str(memory_store_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsMemoryVersionPage.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    memory_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage]:
    """ List memory versions

     Returns a store's change history, newest first, optionally filtered to one memory. Versions belong
    to the store rather than the memory, so the trail survives the memory being deleted. Retained 30
    days, except that the recent versions of a live memory are kept regardless of age.

    Args:
        memory_store_id (UUID): Memory store id (UUID) whose history is being read.
        memory_id (str | Unset): Only versions of this memory. The memory may since have been
            deleted.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.
        cursor (str | Unset): Opaque next_cursor from the previous history page, with the same
            memory_id filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
memory_id=memory_id,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    memory_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage | None:
    """ List memory versions

     Returns a store's change history, newest first, optionally filtered to one memory. Versions belong
    to the store rather than the memory, so the trail survives the memory being deleted. Retained 30
    days, except that the recent versions of a live memory are kept regardless of age.

    Args:
        memory_store_id (UUID): Memory store id (UUID) whose history is being read.
        memory_id (str | Unset): Only versions of this memory. The memory may since have been
            deleted.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.
        cursor (str | Unset): Opaque next_cursor from the previous history page, with the same
            memory_id filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage
     """


    return sync_detailed(
        memory_store_id=memory_store_id,
client=client,
memory_id=memory_id,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    memory_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage]:
    """ List memory versions

     Returns a store's change history, newest first, optionally filtered to one memory. Versions belong
    to the store rather than the memory, so the trail survives the memory being deleted. Retained 30
    days, except that the recent versions of a live memory are kept regardless of age.

    Args:
        memory_store_id (UUID): Memory store id (UUID) whose history is being read.
        memory_id (str | Unset): Only versions of this memory. The memory may since have been
            deleted.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.
        cursor (str | Unset): Opaque next_cursor from the previous history page, with the same
            memory_id filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
memory_id=memory_id,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    memory_id: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage | None:
    """ List memory versions

     Returns a store's change history, newest first, optionally filtered to one memory. Versions belong
    to the store rather than the memory, so the trail survives the memory being deleted. Retained 30
    days, except that the recent versions of a live memory are kept regardless of age.

    Args:
        memory_store_id (UUID): Memory store id (UUID) whose history is being read.
        memory_id (str | Unset): Only versions of this memory. The memory may since have been
            deleted.
        limit (int | Unset): Page size from 1 through 100, default 50. Default: 50.
        cursor (str | Unset): Opaque next_cursor from the previous history page, with the same
            memory_id filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemoryVersionPage
     """


    return (await asyncio_detailed(
        memory_store_id=memory_store_id,
client=client,
memory_id=memory_id,
limit=limit,
cursor=cursor,

    )).parsed
