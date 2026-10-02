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
from ...models.managed_agents_memory import ManagedAgentsMemory
from ...models.managed_agents_memory_create_request import ManagedAgentsMemoryCreateRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    memory_store_id: UUID,
    *,
    body: ManagedAgentsMemoryCreateRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/memory_stores/{memory_store_id}/memories".format(memory_store_id=quote(str(memory_store_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory | None:
    if response.status_code == 201:
        response_201 = ManagedAgentsMemory.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory]:
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
    body: ManagedAgentsMemoryCreateRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory]:
    """ Create a memory

     Adds one memory to a curated store. Does not overwrite: changing an existing path is an update, so a
    retried request cannot destroy content. A store written by the consolidation loop is not hand-
    editable, because editing it would put your text under a provenance saying the platform wrote it and
    the next consolidation would read it as its own prior conclusion.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryCreateRequest): Fields for creating one memory. Path, content and
            summary are all required; omitting any of them is a 400. Example: {'content': 'example',
            'path': 'example', 'summary': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory]
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
    body: ManagedAgentsMemoryCreateRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory | None:
    """ Create a memory

     Adds one memory to a curated store. Does not overwrite: changing an existing path is an update, so a
    retried request cannot destroy content. A store written by the consolidation loop is not hand-
    editable, because editing it would put your text under a provenance saying the platform wrote it and
    the next consolidation would read it as its own prior conclusion.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryCreateRequest): Fields for creating one memory. Path, content and
            summary are all required; omitting any of them is a 400. Example: {'content': 'example',
            'path': 'example', 'summary': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory
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
    body: ManagedAgentsMemoryCreateRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory]:
    """ Create a memory

     Adds one memory to a curated store. Does not overwrite: changing an existing path is an update, so a
    retried request cannot destroy content. A store written by the consolidation loop is not hand-
    editable, because editing it would put your text under a provenance saying the platform wrote it and
    the next consolidation would read it as its own prior conclusion.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryCreateRequest): Fields for creating one memory. Path, content and
            summary are all required; omitting any of them is a 400. Example: {'content': 'example',
            'path': 'example', 'summary': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory]
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
    body: ManagedAgentsMemoryCreateRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory | None:
    """ Create a memory

     Adds one memory to a curated store. Does not overwrite: changing an existing path is an update, so a
    retried request cannot destroy content. A store written by the consolidation loop is not hand-
    editable, because editing it would put your text under a provenance saying the platform wrote it and
    the next consolidation would read it as its own prior conclusion.

    Args:
        memory_store_id (UUID): Memory store id (UUID) as returned by createMemoryStore or
            listMemoryStores.
        body (ManagedAgentsMemoryCreateRequest): Fields for creating one memory. Path, content and
            summary are all required; omitting any of them is a 400. Example: {'content': 'example',
            'path': 'example', 'summary': 'example'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMemory
     """


    return (await asyncio_detailed(
        memory_store_id=memory_store_id,
client=client,
body=body,

    )).parsed
