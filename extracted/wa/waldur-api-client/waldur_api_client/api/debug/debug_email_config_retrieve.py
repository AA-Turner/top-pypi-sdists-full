from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.email_diagnostics import EmailDiagnostics
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/debug/email/config/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> EmailDiagnostics:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = EmailDiagnostics.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[EmailDiagnostics]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[EmailDiagnostics]:
    """Audit the outgoing email configuration

     Reports the effective mail settings and the problems found in them.

    Reads settings only — no connection is opened and no message is sent.
    Covers the two independent halves of email delivery: a usable SMTP relay,
    and at least one enabled notification type. Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailDiagnostics]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> EmailDiagnostics:
    """Audit the outgoing email configuration

     Reports the effective mail settings and the problems found in them.

    Reads settings only — no connection is opened and no message is sent.
    Covers the two independent halves of email delivery: a usable SMTP relay,
    and at least one enabled notification type. Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailDiagnostics
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[EmailDiagnostics]:
    """Audit the outgoing email configuration

     Reports the effective mail settings and the problems found in them.

    Reads settings only — no connection is opened and no message is sent.
    Covers the two independent halves of email delivery: a usable SMTP relay,
    and at least one enabled notification type. Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailDiagnostics]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> EmailDiagnostics:
    """Audit the outgoing email configuration

     Reports the effective mail settings and the problems found in them.

    Reads settings only — no connection is opened and no message is sent.
    Covers the two independent halves of email delivery: a usable SMTP relay,
    and at least one enabled notification type. Requires staff permissions.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailDiagnostics
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
