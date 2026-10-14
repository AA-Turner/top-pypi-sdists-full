from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.web_shell_ticket import WebShellTicket
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/web-shell-ticket/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> WebShellTicket:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = WebShellTicket.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[WebShellTicket]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[WebShellTicket]:
    """Open a web shell session

     Returns a single-use link that opens `waldur shell` in the browser as the calling staff user. Only
    available when the deployment runs with DEBUG and WALDUR_CORE['WEB_SHELL_ENABLED'].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WebShellTicket]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> WebShellTicket:
    """Open a web shell session

     Returns a single-use link that opens `waldur shell` in the browser as the calling staff user. Only
    available when the deployment runs with DEBUG and WALDUR_CORE['WEB_SHELL_ENABLED'].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WebShellTicket
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[WebShellTicket]:
    """Open a web shell session

     Returns a single-use link that opens `waldur shell` in the browser as the calling staff user. Only
    available when the deployment runs with DEBUG and WALDUR_CORE['WEB_SHELL_ENABLED'].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WebShellTicket]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> WebShellTicket:
    """Open a web shell session

     Returns a single-use link that opens `waldur shell` in the browser as the calling staff user. Only
    available when the deployment runs with DEBUG and WALDUR_CORE['WEB_SHELL_ENABLED'].

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WebShellTicket
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
