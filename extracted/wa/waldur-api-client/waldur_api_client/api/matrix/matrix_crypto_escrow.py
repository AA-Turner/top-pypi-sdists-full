from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_crypto_conflict import MatrixCryptoConflict
from ...models.matrix_crypto_escrow_request import MatrixCryptoEscrowRequest
from ...types import Response


def _get_kwargs(
    *,
    body: MatrixCryptoEscrowRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/matrix/crypto/escrow/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, MatrixCryptoConflict]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 409:
        response_409 = MatrixCryptoConflict.from_dict(response.json())

        return response_409
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, MatrixCryptoConflict]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MatrixCryptoEscrowRequest,
) -> Response[Union[Any, MatrixCryptoConflict]]:
    """Escrow the recovery key of chat encryption

     Stores the caller's new secret-storage recovery key. Only the holder of a current lease may; the
    drawer calls this before it uploads any key, so Waldur never loses a key the homeserver depends on.

    Args:
        body (MatrixCryptoEscrowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixCryptoConflict]]
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
    body: MatrixCryptoEscrowRequest,
) -> Union[Any, MatrixCryptoConflict]:
    """Escrow the recovery key of chat encryption

     Stores the caller's new secret-storage recovery key. Only the holder of a current lease may; the
    drawer calls this before it uploads any key, so Waldur never loses a key the homeserver depends on.

    Args:
        body (MatrixCryptoEscrowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixCryptoConflict]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MatrixCryptoEscrowRequest,
) -> Response[Union[Any, MatrixCryptoConflict]]:
    """Escrow the recovery key of chat encryption

     Stores the caller's new secret-storage recovery key. Only the holder of a current lease may; the
    drawer calls this before it uploads any key, so Waldur never loses a key the homeserver depends on.

    Args:
        body (MatrixCryptoEscrowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixCryptoConflict]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: MatrixCryptoEscrowRequest,
) -> Union[Any, MatrixCryptoConflict]:
    """Escrow the recovery key of chat encryption

     Stores the caller's new secret-storage recovery key. Only the holder of a current lease may; the
    drawer calls this before it uploads any key, so Waldur never loses a key the homeserver depends on.

    Args:
        body (MatrixCryptoEscrowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixCryptoConflict]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
