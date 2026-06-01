from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.forwarder_response import ForwarderResponse


def _get_kwargs(
    forwarder_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/forwarders/{forwarder_id}".format(
            forwarder_id=quote(str(forwarder_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ForwarderResponse | None:
    if response.status_code == 200:
        response_200 = ForwarderResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ForwarderResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ForwarderResponse]:
    """Get Forwarder

     Retrieve a single forwarder by id.

    Header values are returned in plaintext so the resource can be
    round-tripped with `GET`, mutate, `PUT` without re-entering secrets.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderResponse]
    """

    kwargs = _get_kwargs(
        forwarder_id=forwarder_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> ForwarderResponse | None:
    """Get Forwarder

     Retrieve a single forwarder by id.

    Header values are returned in plaintext so the resource can be
    round-tripped with `GET`, mutate, `PUT` without re-entering secrets.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderResponse
    """

    return sync_detailed(
        forwarder_id=forwarder_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ForwarderResponse]:
    """Get Forwarder

     Retrieve a single forwarder by id.

    Header values are returned in plaintext so the resource can be
    round-tripped with `GET`, mutate, `PUT` without re-entering secrets.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ForwarderResponse]
    """

    kwargs = _get_kwargs(
        forwarder_id=forwarder_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    forwarder_id: str,
    *,
    client: AuthenticatedClient,
) -> ForwarderResponse | None:
    """Get Forwarder

     Retrieve a single forwarder by id.

    Header values are returned in plaintext so the resource can be
    round-tripped with `GET`, mutate, `PUT` without re-entering secrets.

    Args:
        forwarder_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ForwarderResponse
    """

    return (
        await asyncio_detailed(
            forwarder_id=forwarder_id,
            client=client,
        )
    ).parsed
