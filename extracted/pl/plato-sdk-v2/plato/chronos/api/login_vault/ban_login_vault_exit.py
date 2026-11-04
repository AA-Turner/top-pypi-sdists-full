"""Ban Exit Route"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultExit, LoginVaultExitBanRequest


def _build_request_args(
    name: str,
    body: LoginVaultExitBanRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/exits/{name}/ban"

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    name: str,
    body: LoginVaultExitBanRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExit:
    """Ban the exit for one app (`login_key`), or for every app (`login_key` absent, `""` or `*`): the next run of that app that asks for its upstream is refused. A ban for every app replaces the exit's per-app bans; an exit banned for every app stays so. `reason` (optional, one line of at most 200) is kept with who and when. A ban already in force writes nothing (its first reason stands). Answers the exit's row. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        name=name,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultExit.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    name: str,
    body: LoginVaultExitBanRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExit:
    """Ban the exit for one app (`login_key`), or for every app (`login_key` absent, `""` or `*`): the next run of that app that asks for its upstream is refused. A ban for every app replaces the exit's per-app bans; an exit banned for every app stays so. `reason` (optional, one line of at most 200) is kept with who and when. A ban already in force writes nothing (its first reason stands). Answers the exit's row. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        name=name,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultExit.model_validate(response.json())
