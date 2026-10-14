from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_recovery_key import MatrixRecoveryKey
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/matrix/credentials/recovery-key/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, MatrixRecoveryKey]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MatrixRecoveryKey.from_dict(response.json())

        return response_200
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, MatrixRecoveryKey]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, MatrixRecoveryKey]]:
    """Show the recovery key of chat encryption

     Returns the caller's escrowed recovery key, so that another Matrix client, such as Element, can
    unlock their encrypted history. Only a key that opens the user's secret storage on the homeserver is
    returned; null otherwise. A POST, as each reveal is recorded in the user's event log.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixRecoveryKey]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Union[Any, MatrixRecoveryKey]:
    """Show the recovery key of chat encryption

     Returns the caller's escrowed recovery key, so that another Matrix client, such as Element, can
    unlock their encrypted history. Only a key that opens the user's secret storage on the homeserver is
    returned; null otherwise. A POST, as each reveal is recorded in the user's event log.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixRecoveryKey]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, MatrixRecoveryKey]]:
    """Show the recovery key of chat encryption

     Returns the caller's escrowed recovery key, so that another Matrix client, such as Element, can
    unlock their encrypted history. Only a key that opens the user's secret storage on the homeserver is
    returned; null otherwise. A POST, as each reveal is recorded in the user's event log.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, MatrixRecoveryKey]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Union[Any, MatrixRecoveryKey]:
    """Show the recovery key of chat encryption

     Returns the caller's escrowed recovery key, so that another Matrix client, such as Element, can
    unlock their encrypted history. Only a key that opens the user's secret storage on the homeserver is
    returned; null otherwise. A POST, as each reveal is recorded in the user's event log.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, MatrixRecoveryKey]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
