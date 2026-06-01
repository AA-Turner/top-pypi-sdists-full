from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors


def _get_kwargs(
    token: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/exports/{token}".format(
            token=quote(str(token), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """Download Export

     Stream a signed audit-events download — no `Authorization` header required.

    Authorization is the token itself: it carries the account, the
    chosen format, and the filters, all integrity-protected by HMAC.
    The endpoint verifies the signature and expiry, scopes the events
    query to the token's account, and streams the response.

    Any failure (bad signature, wrong audience, expired, malformed
    payload) returns `404 Not Found` — the response shape never leaks
    which check failed.

    The token is stateless and replayable until it expires (≤30s).
    Concurrent or duplicate GETs (browser retries, AV scanners,
    prefetchers) all succeed; there is no single-use behavior.

    Args:
        token (str): Opaque signed download token from `POST /api/v1/exports`. Treat as a single
            short-lived URL — do not parse or store long-term.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        token=token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    token: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """Download Export

     Stream a signed audit-events download — no `Authorization` header required.

    Authorization is the token itself: it carries the account, the
    chosen format, and the filters, all integrity-protected by HMAC.
    The endpoint verifies the signature and expiry, scopes the events
    query to the token's account, and streams the response.

    Any failure (bad signature, wrong audience, expired, malformed
    payload) returns `404 Not Found` — the response shape never leaks
    which check failed.

    The token is stateless and replayable until it expires (≤30s).
    Concurrent or duplicate GETs (browser retries, AV scanners,
    prefetchers) all succeed; there is no single-use behavior.

    Args:
        token (str): Opaque signed download token from `POST /api/v1/exports`. Treat as a single
            short-lived URL — do not parse or store long-term.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        token=token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
