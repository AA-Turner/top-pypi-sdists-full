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
from typing import cast
from uuid import UUID



def _get_kwargs(
    memory_store_id: UUID,
    memory_version_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact".format(memory_store_id=quote(str(memory_store_id), safe=""),memory_version_id=quote(str(memory_version_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    memory_store_id: UUID,
    memory_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    """ Redact a memory version

     Scrubs a historical version's content while preserving who wrote it and when, for compliance
    workflows such as removing a leaked secret. Refuses a version that is the live content of a memory:
    write a replacement first, then redact the old one.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the version belongs to.
        memory_version_id (UUID): Memory version id (UUID) as returned by listMemoryVersions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
memory_version_id=memory_version_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    memory_store_id: UUID,
    memory_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    """ Redact a memory version

     Scrubs a historical version's content while preserving who wrote it and when, for compliance
    workflows such as removing a leaked secret. Refuses a version that is the live content of a memory:
    write a replacement first, then redact the old one.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the version belongs to.
        memory_version_id (UUID): Memory version id (UUID) as returned by listMemoryVersions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout
     """


    return sync_detailed(
        memory_store_id=memory_store_id,
memory_version_id=memory_version_id,
client=client,

    ).parsed

async def asyncio_detailed(
    memory_store_id: UUID,
    memory_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    """ Redact a memory version

     Scrubs a historical version's content while preserving who wrote it and when, for compliance
    workflows such as removing a leaked secret. Refuses a version that is the live content of a memory:
    write a replacement first, then redact the old one.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the version belongs to.
        memory_version_id (UUID): Memory version id (UUID) as returned by listMemoryVersions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        memory_store_id=memory_store_id,
memory_version_id=memory_version_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    memory_store_id: UUID,
    memory_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    """ Redact a memory version

     Scrubs a historical version's content while preserving who wrote it and when, for compliance
    workflows such as removing a leaked secret. Refuses a version that is the live content of a memory:
    write a replacement first, then redact the old one.

    Args:
        memory_store_id (UUID): Memory store id (UUID) the version belongs to.
        memory_version_id (UUID): Memory version id (UUID) as returned by listMemoryVersions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout
     """


    return (await asyncio_detailed(
        memory_store_id=memory_store_id,
memory_version_id=memory_version_id,
client=client,

    )).parsed
