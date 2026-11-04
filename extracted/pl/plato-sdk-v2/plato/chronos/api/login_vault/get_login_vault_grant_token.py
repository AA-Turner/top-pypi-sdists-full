"""Read Grant Token"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultGrantToken


def _build_request_args(
    login_key: str,
    account: str,
    kind: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/accounts/{login_key}/{account}/grants/{kind}/token"

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    login_key: str,
    account: str,
    kind: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultGrantToken:
    """The access token and its expiry, never the refresh token. An active grant with less than 30 minutes left is refreshed first (a concurrent read waits for that refresh). 404 when there is no grant or no access token; 409 when it is not active and its token has expired, or a refresh never stored its result; 502 when the vendor refused the refresh or gave no clear answer. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        kind=kind,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultGrantToken.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    account: str,
    kind: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultGrantToken:
    """The access token and its expiry, never the refresh token. An active grant with less than 30 minutes left is refreshed first (a concurrent read waits for that refresh). 404 when there is no grant or no access token; 409 when it is not active and its token has expired, or a refresh never stored its result; 502 when the vendor refused the refresh or gave no clear answer. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        kind=kind,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultGrantToken.model_validate(response.json())
