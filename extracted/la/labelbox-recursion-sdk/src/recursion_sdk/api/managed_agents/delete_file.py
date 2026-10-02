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
from ...models.managed_agents_deleted_response import ManagedAgentsDeletedResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    file_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/managed-agents/v1/files/{file_id}".format(file_id=quote(str(file_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsDeletedResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse]:
    """ Delete a file

     Deletes the file's metadata at once; new attachments and reads answer 404. The stored bytes are
    reclaimed after a grace, and only when no other file of the organization names the same content. Not
    a revocation until then: a session that attached the file before froze its digest and stages by that
    digest, so the bytes still reach that session's sandbox on its later turns, resumes, and replacement
    sandboxes for as long as the object lasts; after reclaim, staging warns and continues without it.

    Args:
        file_id (UUID): File id (UUID) as returned by uploadFile or listFiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse]
     """


    kwargs = _get_kwargs(
        file_id=file_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse | None:
    """ Delete a file

     Deletes the file's metadata at once; new attachments and reads answer 404. The stored bytes are
    reclaimed after a grace, and only when no other file of the organization names the same content. Not
    a revocation until then: a session that attached the file before froze its digest and stages by that
    digest, so the bytes still reach that session's sandbox on its later turns, resumes, and replacement
    sandboxes for as long as the object lasts; after reclaim, staging warns and continues without it.

    Args:
        file_id (UUID): File id (UUID) as returned by uploadFile or listFiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse
     """


    return sync_detailed(
        file_id=file_id,
client=client,

    ).parsed

async def asyncio_detailed(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse]:
    """ Delete a file

     Deletes the file's metadata at once; new attachments and reads answer 404. The stored bytes are
    reclaimed after a grace, and only when no other file of the organization names the same content. Not
    a revocation until then: a session that attached the file before froze its digest and stages by that
    digest, so the bytes still reach that session's sandbox on its later turns, resumes, and replacement
    sandboxes for as long as the object lasts; after reclaim, staging warns and continues without it.

    Args:
        file_id (UUID): File id (UUID) as returned by uploadFile or listFiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse]
     """


    kwargs = _get_kwargs(
        file_id=file_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    file_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse | None:
    """ Delete a file

     Deletes the file's metadata at once; new attachments and reads answer 404. The stored bytes are
    reclaimed after a grace, and only when no other file of the organization names the same content. Not
    a revocation until then: a session that attached the file before froze its digest and stages by that
    digest, so the bytes still reach that session's sandbox on its later turns, resumes, and replacement
    sandboxes for as long as the object lasts; after reclaim, staging warns and continues without it.

    Args:
        file_id (UUID): File id (UUID) as returned by uploadFile or listFiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsDeletedResponse
     """


    return (await asyncio_detailed(
        file_id=file_id,
client=client,

    )).parsed
