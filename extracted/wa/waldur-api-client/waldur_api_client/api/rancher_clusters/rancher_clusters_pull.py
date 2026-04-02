from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pull_conflict_response import PullConflictResponse
from ...models.pull_response import PullResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/rancher-clusters/{uuid}/pull/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[PullConflictResponse, PullResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 202:
        response_202 = PullResponse.from_dict(response.json())

        return response_202
    if response.status_code == 409:
        response_409 = PullConflictResponse.from_dict(response.json())

        return response_409
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[PullConflictResponse, PullResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[PullConflictResponse, PullResponse]]:
    """Synchronize resource state

     Schedule an asynchronous pull operation to synchronize resource state from the backend. Returns 202
    if the pull was scheduled successfully, or 409 if the pull operation is not implemented for this
    resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PullConflictResponse, PullResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Union[PullConflictResponse, PullResponse]:
    """Synchronize resource state

     Schedule an asynchronous pull operation to synchronize resource state from the backend. Returns 202
    if the pull was scheduled successfully, or 409 if the pull operation is not implemented for this
    resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PullConflictResponse, PullResponse]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[PullConflictResponse, PullResponse]]:
    """Synchronize resource state

     Schedule an asynchronous pull operation to synchronize resource state from the backend. Returns 202
    if the pull was scheduled successfully, or 409 if the pull operation is not implemented for this
    resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PullConflictResponse, PullResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Union[PullConflictResponse, PullResponse]:
    """Synchronize resource state

     Schedule an asynchronous pull operation to synchronize resource state from the backend. Returns 202
    if the pull was scheduled successfully, or 409 if the pull operation is not implemented for this
    resource type.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PullConflictResponse, PullResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
