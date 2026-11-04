"""Get Default"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultDefault


def _build_request_args(
    clone: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/defaults/{clone}"

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
    clone: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultDefault:
    """One clone's default account. `login_key` and `account` are null when it has none. Every vault-org key."""

    request_args = _build_request_args(
        clone=clone,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultDefault.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    clone: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultDefault:
    """One clone's default account. `login_key` and `account` are null when it has none. Every vault-org key."""

    request_args = _build_request_args(
        clone=clone,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultDefault.model_validate(response.json())
