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
from ...models.managed_agents_memory import ManagedAgentsMemory
from typing import cast
from uuid import UUID



def _get_kwargs(
    memory_store_id: UUID,
    *,
    path: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["path"] = path


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/memory_stores/{memory_store_id}/memory".format(memory_store_id=quote(str(memory_store_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsMemory.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory]:
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
    path: str,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory]:
    """ Read one memory by path

     Returns one memory including its full content, addressed by the path a listing or search returned. A
    separate route from the id-addressed read so each has one response shape; use this one when you are
    following a listing, which is the common case.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the memory belongs to.
        path (str): Path of the memory, exactly as a listing or search returned it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
path=path,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    path: str,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory | None:
    """ Read one memory by path

     Returns one memory including its full content, addressed by the path a listing or search returned. A
    separate route from the id-addressed read so each has one response shape; use this one when you are
    following a listing, which is the common case.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the memory belongs to.
        path (str): Path of the memory, exactly as a listing or search returned it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory
     """


    return sync_detailed(
        memory_store_id=memory_store_id,
client=client,
path=path,

    ).parsed

async def asyncio_detailed(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    path: str,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory]:
    """ Read one memory by path

     Returns one memory including its full content, addressed by the path a listing or search returned. A
    separate route from the id-addressed read so each has one response shape; use this one when you are
    following a listing, which is the common case.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the memory belongs to.
        path (str): Path of the memory, exactly as a listing or search returned it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
path=path,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    path: str,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory | None:
    """ Read one memory by path

     Returns one memory including its full content, addressed by the path a listing or search returned. A
    separate route from the id-addressed read so each has one response shape; use this one when you are
    following a listing, which is the common case.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the memory belongs to.
        path (str): Path of the memory, exactly as a listing or search returned it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsMemory
     """


    return (await asyncio_detailed(
        memory_store_id=memory_store_id,
client=client,
path=path,

    )).parsed
