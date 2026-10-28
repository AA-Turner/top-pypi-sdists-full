"""Get Account Persona"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAccountPersona


def _build_request_args(
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/accounts/{login_key}/{account}/persona"

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
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersona:
    """Who the account is: `person_key` (the persona it is linked to), `live` (what the real account shows on the app, each value with its `source`, or a `note` when null) and, from the linked persona, its `fixture`, `email`, `inbox` and `phone`. 404 `no persona` when the account has neither a link nor live values, and for an unknown account (an item made by hand is adopted first). Archived accounts are readable. 502/503 when 1Password cannot answer. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersona.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersona:
    """Who the account is: `person_key` (the persona it is linked to), `live` (what the real account shows on the app, each value with its `source`, or a `note` when null) and, from the linked persona, its `fixture`, `email`, `inbox` and `phone`. 404 `no persona` when the account has neither a link nor live values, and for an unknown account (an item made by hand is adopted first). Archived accounts are readable. 502/503 when 1Password cannot answer. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersona.model_validate(response.json())
