"""List Defaults"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultDefaults


def _build_request_args(
    clone: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/login-vault/defaults"

    params: dict[str, Any] = {}
    if clone is not None:
        params["clone"] = clone

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
    clone: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultDefaults:
    """Which account each clone logs in as by default: `{defaults: {clone: {login_key, account}}}`. `clone` narrows it to one clone. A clone with no default is left out. Every vault-org key."""

    request_args = _build_request_args(
        clone=clone,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultDefaults.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    clone: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultDefaults:
    """Which account each clone logs in as by default: `{defaults: {clone: {login_key, account}}}`. `clone` narrows it to one clone. A clone with no default is left out. Every vault-org key."""

    request_args = _build_request_args(
        clone=clone,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultDefaults.model_validate(response.json())
