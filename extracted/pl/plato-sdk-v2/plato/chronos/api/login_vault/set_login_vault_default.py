"""Set Default"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultDefault, LoginVaultDefaultUpdate


def _build_request_args(
    clone: str,
    body: LoginVaultDefaultUpdate,
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
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    clone: str,
    body: LoginVaultDefaultUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultDefault:
    """Make an account the clone's default login (`{login_key, account}`), or clear the clone's default (both null). A value it already holds writes nothing. 404 when the vault has no such account; 409 when it is archived. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        clone=clone,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultDefault.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    clone: str,
    body: LoginVaultDefaultUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultDefault:
    """Make an account the clone's default login (`{login_key, account}`), or clear the clone's default (both null). A value it already holds writes nothing. 404 when the vault has no such account; 409 when it is archived. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        clone=clone,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultDefault.model_validate(response.json())
