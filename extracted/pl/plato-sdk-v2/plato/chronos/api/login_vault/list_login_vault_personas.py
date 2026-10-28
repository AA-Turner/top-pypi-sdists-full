"""List Personas Route"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultPersonaList


def _build_request_args(
    limit: int | None = 100,
    cursor: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/login-vault/personas"

    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if cursor is not None:
        params["cursor"] = cursor

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    limit: int | None = 100,
    cursor: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultPersonaList:
    """Every persona (an email, the 1Password mail item its mail lands in, and a phone), by key. `phone_status` is read live from the `sms-` items: `active`, `deprecated` (retired by the TextVerified sync), `unknown` (no `sms-` item holds the number), or null with no phone. One page at a time, by key; `next_cursor` fetches the next. 502/503 when 1Password cannot answer. Every vault-org key."""

    request_args = _build_request_args(
        limit=limit,
        cursor=cursor,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultPersonaList.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    limit: int | None = 100,
    cursor: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultPersonaList:
    """Every persona (an email, the 1Password mail item its mail lands in, and a phone), by key. `phone_status` is read live from the `sms-` items: `active`, `deprecated` (retired by the TextVerified sync), `unknown` (no `sms-` item holds the number), or null with no phone. One page at a time, by key; `next_cursor` fetches the next. 502/503 when 1Password cannot answer. Every vault-org key."""

    request_args = _build_request_args(
        limit=limit,
        cursor=cursor,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultPersonaList.model_validate(response.json())
