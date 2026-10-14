from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.email_probe import EmailProbe
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/debug/email/probe/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> EmailProbe:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = EmailProbe.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[EmailProbe]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[EmailProbe]:
    """Test the SMTP connection

     Opens and closes a connection to the configured relay without sending a message.

    The connection is made from the API process, which may reach the network
    differently than the Celery workers that send real notifications.
    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailProbe]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> EmailProbe:
    """Test the SMTP connection

     Opens and closes a connection to the configured relay without sending a message.

    The connection is made from the API process, which may reach the network
    differently than the Celery workers that send real notifications.
    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailProbe
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[EmailProbe]:
    """Test the SMTP connection

     Opens and closes a connection to the configured relay without sending a message.

    The connection is made from the API process, which may reach the network
    differently than the Celery workers that send real notifications.
    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailProbe]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> EmailProbe:
    """Test the SMTP connection

     Opens and closes a connection to the configured relay without sending a message.

    The connection is made from the API process, which may reach the network
    differently than the Celery workers that send real notifications.
    Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailProbe
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
