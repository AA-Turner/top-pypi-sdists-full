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
from ...models.managed_agents_memory_store import ManagedAgentsMemoryStore
from ...models.managed_agents_memory_store_request import ManagedAgentsMemoryStoreRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    memory_store_id: UUID,
    *,
    body: ManagedAgentsMemoryStoreRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/memory_stores/{memory_store_id}".format(memory_store_id=quote(str(memory_store_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsMemoryStore.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore]:
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
    body: ManagedAgentsMemoryStoreRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore]:
    """ Update a memory store

     Renames a store or changes its description. An omitted field is left unchanged. An archived store is
    immutable.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryStoreRequest): Fields for creating or renaming a curated memory
            store. An omitted field is left unchanged on update. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'description': 'example', 'name': 'example-name'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsMemoryStoreRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore | None:
    """ Update a memory store

     Renames a store or changes its description. An omitted field is left unchanged. An archived store is
    immutable.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryStoreRequest): Fields for creating or renaming a curated memory
            store. An omitted field is left unchanged on update. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'description': 'example', 'name': 'example-name'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore
     """


    return sync_detailed(
        memory_store_id=memory_store_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsMemoryStoreRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore]:
    """ Update a memory store

     Renames a store or changes its description. An omitted field is left unchanged. An archived store is
    immutable.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryStoreRequest): Fields for creating or renaming a curated memory
            store. An omitted field is left unchanged on update. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'description': 'example', 'name': 'example-name'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    memory_store_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsMemoryStoreRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore | None:
    """ Update a memory store

     Renames a store or changes its description. An omitted field is left unchanged. An archived store is
    immutable.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryStoreRequest): Fields for creating or renaming a curated memory
            store. An omitted field is left unchanged on update. Example: {'agent_id':
            '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'description': 'example', 'name': 'example-name'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemoryStore
     """


    return (await asyncio_detailed(
        memory_store_id=memory_store_id,
client=client,
body=body,

    )).parsed
