"""Delete Account Persona"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAccountPersonaDeleted


def _build_request_args(
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/accounts/{login_key}/{account}/persona"

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersonaDeleted:
    """Unlink the account from its persona and clear its live identity. The persona itself stays (it is the person, and its other accounts keep it). `deleted`: whether there was anything to clear. 404 for an unknown account, 409 for an archived one. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersonaDeleted.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersonaDeleted:
    """Unlink the account from its persona and clear its live identity. The persona itself stays (it is the person, and its other accounts keep it). `deleted`: whether there was anything to clear. 404 for an unknown account, 409 for an archived one. Every vault-org key."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersonaDeleted.model_validate(response.json())
