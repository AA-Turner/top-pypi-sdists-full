"""Unban Exit Route"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultExit, LoginVaultExitUnbanRequest


def _build_request_args(
    name: str,
    body: LoginVaultExitUnbanRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/exits/{name}/unban"

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
    body: LoginVaultExitUnbanRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExit:
    """Lift the exit's ban for one app (`login_key`), or the whole ban (`login_key` absent, `""` or `*`). 409 when lifting one app from an exit banned for every app: lift the whole ban, then ban it again for the apps it is still burned on. An exit not banned for that app writes nothing. Answers the exit's row. Every key of the vault org (person, org-wide, run)."""

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
    body: LoginVaultExitUnbanRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExit:
    """Lift the exit's ban for one app (`login_key`), or the whole ban (`login_key` absent, `""` or `*`). 409 when lifting one app from an exit banned for every app: lift the whole ban, then ban it again for the apps it is still burned on. An exit not banned for that app writes nothing. Answers the exit's row. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        name=name,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultExit.model_validate(response.json())
