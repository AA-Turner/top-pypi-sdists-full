from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.posix_id_pool_repoint import PosixIdPoolRepoint
from ...models.posix_id_pool_repoint_request_request import PosixIdPoolRepointRequestRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: PosixIdPoolRepointRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-posix-id-pools/{uuid}/repoint/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> PosixIdPoolRepoint:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = PosixIdPoolRepoint.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PosixIdPoolRepoint]:
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
    body: PosixIdPoolRepointRequestRequest,
) -> Response[PosixIdPoolRepoint]:
    """Re-point existing accounts onto this pool

     Moves the offering's existing accounts onto this override pool and returns the identifiers that
    changed. Requires 'confirm': true - preview the impact with repoint_preview first, and reconcile the
    provider's filesystem afterwards, since the accounts' files still carry the old numbers. Values
    freed in the previously resolved pool are withheld from recycling until an operator returns them.
    Offering-level pools only.

    Args:
        uuid (UUID):
        body (PosixIdPoolRepointRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PosixIdPoolRepoint]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PosixIdPoolRepointRequestRequest,
) -> PosixIdPoolRepoint:
    """Re-point existing accounts onto this pool

     Moves the offering's existing accounts onto this override pool and returns the identifiers that
    changed. Requires 'confirm': true - preview the impact with repoint_preview first, and reconcile the
    provider's filesystem afterwards, since the accounts' files still carry the old numbers. Values
    freed in the previously resolved pool are withheld from recycling until an operator returns them.
    Offering-level pools only.

    Args:
        uuid (UUID):
        body (PosixIdPoolRepointRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PosixIdPoolRepoint
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PosixIdPoolRepointRequestRequest,
) -> Response[PosixIdPoolRepoint]:
    """Re-point existing accounts onto this pool

     Moves the offering's existing accounts onto this override pool and returns the identifiers that
    changed. Requires 'confirm': true - preview the impact with repoint_preview first, and reconcile the
    provider's filesystem afterwards, since the accounts' files still carry the old numbers. Values
    freed in the previously resolved pool are withheld from recycling until an operator returns them.
    Offering-level pools only.

    Args:
        uuid (UUID):
        body (PosixIdPoolRepointRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PosixIdPoolRepoint]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: PosixIdPoolRepointRequestRequest,
) -> PosixIdPoolRepoint:
    """Re-point existing accounts onto this pool

     Moves the offering's existing accounts onto this override pool and returns the identifiers that
    changed. Requires 'confirm': true - preview the impact with repoint_preview first, and reconcile the
    provider's filesystem afterwards, since the accounts' files still carry the old numbers. Values
    freed in the previously resolved pool are withheld from recycling until an operator returns them.
    Offering-level pools only.

    Args:
        uuid (UUID):
        body (PosixIdPoolRepointRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PosixIdPoolRepoint
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
