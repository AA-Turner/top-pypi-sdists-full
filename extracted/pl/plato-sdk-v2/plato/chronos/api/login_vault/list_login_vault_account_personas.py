"""List Account Personas"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAccountPersonaList


def _build_request_args(
    login_key: str | None = None,
    limit: int | None = 100,
    cursor: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/login-vault/account-personas"

    params: dict[str, Any] = {}
    if login_key is not None:
        params["login_key"] = login_key
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
    login_key: str | None = None,
    limit: int | None = 100,
    cursor: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersonaList:
    """Who each live account is: every account that is not archived and is linked to a persona or has live values (only `login_key`'s when given), with its linked persona's fixture, email, inbox and phone, by (login_key, account). `phone_status` is read live from the `sms-` items: 502/503 when 1Password cannot answer. One page at a time; `next_cursor` fetches the next. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        limit=limit,
        cursor=cursor,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersonaList.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str | None = None,
    limit: int | None = 100,
    cursor: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersonaList:
    """Who each live account is: every account that is not archived and is linked to a persona or has live values (only `login_key`'s when given), with its linked persona's fixture, email, inbox and phone, by (login_key, account). `phone_status` is read live from the `sms-` items: 502/503 when 1Password cannot answer. One page at a time; `next_cursor` fetches the next. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        limit=limit,
        cursor=cursor,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersonaList.model_validate(response.json())
