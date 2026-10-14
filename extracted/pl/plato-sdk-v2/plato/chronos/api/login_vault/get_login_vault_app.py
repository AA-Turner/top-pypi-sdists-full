"""Get App"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAppHint


def _build_request_args(
    login_key: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/apps/{login_key}"

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
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAppHint:
    """The sign-in flow every account of the app shares; `login_hint` is null when none is recorded. A bake gets it, then the account's own `login_hint`, joined by a blank line. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAppHint.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAppHint:
    """The sign-in flow every account of the app shares; `login_hint` is null when none is recorded. A bake gets it, then the account's own `login_hint`, joined by a blank line. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAppHint.model_validate(response.json())
