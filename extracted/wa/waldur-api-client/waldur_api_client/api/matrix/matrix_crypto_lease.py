from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_crypto_conflict import MatrixCryptoConflict
from ...models.matrix_crypto_lease import MatrixCryptoLease
from ...models.matrix_crypto_lease_request_request import MatrixCryptoLeaseRequestRequest
from ...types import Response


def _get_kwargs(
    *,
    body: MatrixCryptoLeaseRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/matrix/crypto/lease/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, MatrixCryptoConflict, MatrixCryptoLease]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MatrixCryptoLease.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 409:
        response_409 = MatrixCryptoConflict.from_dict(response.json())

        return response_409
    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, MatrixCryptoConflict, MatrixCryptoLease]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MatrixCryptoLeaseRequestRequest,
) -> Response[Union[Any, MatrixCryptoConflict, MatrixCryptoLease]]:
    """Take the lease to set up or reset chat encryption

     Admits one browser at a time to setting up the caller's end-to-end encryption (`bootstrap`), or to
    replacing an identity Waldur can't unlock (`reset`). A reset also returns a temporary password for
    the homeserver's interactive auth; it is replaced once the new recovery key is escrowed, or when the
    lease runs out. 409 says why the request can't proceed: `set_up`, `locked` (set up without a key
    Waldur holds), `not_locked`, or `in_progress` (with Retry-After).

    Args:
        body (MatrixCryptoLeaseRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixCryptoConflict, MatrixCryptoLease]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: MatrixCryptoLeaseRequestRequest,
) -> Union[Any, MatrixCryptoConflict, MatrixCryptoLease]:
    """Take the lease to set up or reset chat encryption

     Admits one browser at a time to setting up the caller's end-to-end encryption (`bootstrap`), or to
    replacing an identity Waldur can't unlock (`reset`). A reset also returns a temporary password for
    the homeserver's interactive auth; it is replaced once the new recovery key is escrowed, or when the
    lease runs out. 409 says why the request can't proceed: `set_up`, `locked` (set up without a key
    Waldur holds), `not_locked`, or `in_progress` (with Retry-After).

    Args:
        body (MatrixCryptoLeaseRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixCryptoConflict, MatrixCryptoLease]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MatrixCryptoLeaseRequestRequest,
) -> Response[Union[Any, MatrixCryptoConflict, MatrixCryptoLease]]:
    """Take the lease to set up or reset chat encryption

     Admits one browser at a time to setting up the caller's end-to-end encryption (`bootstrap`), or to
    replacing an identity Waldur can't unlock (`reset`). A reset also returns a temporary password for
    the homeserver's interactive auth; it is replaced once the new recovery key is escrowed, or when the
    lease runs out. 409 says why the request can't proceed: `set_up`, `locked` (set up without a key
    Waldur holds), `not_locked`, or `in_progress` (with Retry-After).

    Args:
        body (MatrixCryptoLeaseRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixCryptoConflict, MatrixCryptoLease]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: MatrixCryptoLeaseRequestRequest,
) -> Union[Any, MatrixCryptoConflict, MatrixCryptoLease]:
    """Take the lease to set up or reset chat encryption

     Admits one browser at a time to setting up the caller's end-to-end encryption (`bootstrap`), or to
    replacing an identity Waldur can't unlock (`reset`). A reset also returns a temporary password for
    the homeserver's interactive auth; it is replaced once the new recovery key is escrowed, or when the
    lease runs out. 409 says why the request can't proceed: `set_up`, `locked` (set up without a key
    Waldur holds), `not_locked`, or `in_progress` (with Retry-After).

    Args:
        body (MatrixCryptoLeaseRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixCryptoConflict, MatrixCryptoLease]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
