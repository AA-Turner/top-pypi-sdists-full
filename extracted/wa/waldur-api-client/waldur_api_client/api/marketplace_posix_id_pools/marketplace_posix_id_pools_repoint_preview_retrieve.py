from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.posix_id_pool_repoint import PosixIdPoolRepoint
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-posix-id-pools/{uuid}/repoint_preview/",
    }

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
) -> Response[PosixIdPoolRepoint]:
    """Preview re-pointing existing accounts onto this pool

     Adding an override pool to an offering that already has accounts changes nothing by itself: accounts
    created afterwards draw from the override pool, while existing ones keep the values they were given
    by the previously resolved pool. This action reports which offering users would change and from
    which value to which, without writing anything. Offering-level pools only.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PosixIdPoolRepoint]
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
) -> PosixIdPoolRepoint:
    """Preview re-pointing existing accounts onto this pool

     Adding an override pool to an offering that already has accounts changes nothing by itself: accounts
    created afterwards draw from the override pool, while existing ones keep the values they were given
    by the previously resolved pool. This action reports which offering users would change and from
    which value to which, without writing anything. Offering-level pools only.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PosixIdPoolRepoint
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[PosixIdPoolRepoint]:
    """Preview re-pointing existing accounts onto this pool

     Adding an override pool to an offering that already has accounts changes nothing by itself: accounts
    created afterwards draw from the override pool, while existing ones keep the values they were given
    by the previously resolved pool. This action reports which offering users would change and from
    which value to which, without writing anything. Offering-level pools only.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PosixIdPoolRepoint]
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
) -> PosixIdPoolRepoint:
    """Preview re-pointing existing accounts onto this pool

     Adding an override pool to an offering that already has accounts changes nothing by itself: accounts
    created afterwards draw from the override pool, while existing ones keep the values they were given
    by the previously resolved pool. This action reports which offering users would change and from
    which value to which, without writing anything. Offering-level pools only.

    Args:
        uuid (UUID):

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
        )
    ).parsed
