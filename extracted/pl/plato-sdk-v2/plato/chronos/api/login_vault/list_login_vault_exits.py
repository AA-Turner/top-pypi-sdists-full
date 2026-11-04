"""List Exits"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultExitList


def _build_request_args(
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/login-vault/exits"

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
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExitList:
    """Every proxy exit: those the provider items define (`brd-<ip>`, `decodo-<port>`, `home`), then any name an account binding or a ban uses that they do not (`in_registry: false`). Each with its bans (`login_key` `*` = every app; `reason`, `by` and `at` when known) and the accounts bound to it (archived ones too, flagged). No provider credentials. Bans are read fresh. Every vault-org key."""

    request_args = _build_request_args(
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultExitList.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExitList:
    """Every proxy exit: those the provider items define (`brd-<ip>`, `decodo-<port>`, `home`), then any name an account binding or a ban uses that they do not (`in_registry: false`). Each with its bans (`login_key` `*` = every app; `reason`, `by` and `at` when known) and the accounts bound to it (archived ones too, flagged). No provider credentials. Bans are read fresh. Every vault-org key."""

    request_args = _build_request_args(
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultExitList.model_validate(response.json())
