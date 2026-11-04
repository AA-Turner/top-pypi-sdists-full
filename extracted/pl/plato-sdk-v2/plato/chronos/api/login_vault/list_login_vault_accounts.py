"""List Accounts"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAccountList


def _build_request_args(
    login_key: str | None = None,
    include_archived: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/login-vault/accounts"

    params: dict[str, Any] = {}
    if login_key is not None:
        params["login_key"] = login_key
    if include_archived is not None:
        params["include_archived"] = include_archived

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
    include_archived: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountList:
    """Every account, from the rows - no password, TOTP seed or security answer.

    Items made by hand in 1Password since the last look are adopted first: the
    vault's titles are listed at most once a minute per process (and only the
    new items read). The list still answers when 1Password cannot, with
    ``vault_error`` set: items made by hand may be missing from it.
    Archived accounts are left out unless ``include_archived``."""

    request_args = _build_request_args(
        login_key=login_key,
        include_archived=include_archived,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountList.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str | None = None,
    include_archived: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountList:
    """Every account, from the rows - no password, TOTP seed or security answer.

    Items made by hand in 1Password since the last look are adopted first: the
    vault's titles are listed at most once a minute per process (and only the
    new items read). The list still answers when 1Password cannot, with
    ``vault_error`` set: items made by hand may be missing from it.
    Archived accounts are left out unless ``include_archived``."""

    request_args = _build_request_args(
        login_key=login_key,
        include_archived=include_archived,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountList.model_validate(response.json())
