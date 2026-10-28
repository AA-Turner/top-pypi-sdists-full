"""List Free Personas"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultFreePersonas


def _build_request_args(
    login_key: str,
    all: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/login-vault/free"

    params: dict[str, Any] = {}
    if login_key is not None:
        params["login_key"] = login_key
    if all is not None:
        params["all"] = all

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
    login_key: str,
    all: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultFreePersonas:
    """The personas free to sign up to the app `login_key`: no live account of the app is linked to the persona or has its email as its username (`has_account`), its number is not retired (`number_deprecated`), and no other live account of the app holds its number (`number_on_app`), in that precedence; `accounts` names the accounts in the way. A persona with no phone can be free. Archived accounts do not count; account items made by hand in 1Password are adopted first. Only the `free` ones by default; `all=true` answers every persona with its `state`, free first, then by key. Fails closed: 502/503 when 1Password cannot answer. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        all=all,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultFreePersonas.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    all: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultFreePersonas:
    """The personas free to sign up to the app `login_key`: no live account of the app is linked to the persona or has its email as its username (`has_account`), its number is not retired (`number_deprecated`), and no other live account of the app holds its number (`number_on_app`), in that precedence; `accounts` names the accounts in the way. A persona with no phone can be free. Archived accounts do not count; account items made by hand in 1Password are adopted first. Only the `free` ones by default; `all=true` answers every persona with its `state`, free first, then by key. Fails closed: 502/503 when 1Password cannot answer. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        all=all,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultFreePersonas.model_validate(response.json())
