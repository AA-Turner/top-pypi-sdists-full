"""Update Account"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAccount, LoginVaultAccountUpdate


def _build_request_args(
    login_key: str,
    account: str,
    body: LoginVaultAccountUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/accounts/{login_key}/{account}"

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PATCH",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    login_key: str,
    account: str,
    body: LoginVaultAccountUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccount:
    """Change some fields: absent/null = leave, ``""`` = clear, a value = set.

    The secrets are written to the 1Password item, the settings to the row. A
    real change also stamps the row's ``updated_by`` with the caller. 409 while
    the account is archived (restore it first). 422 when a new ``proxy_exit`` is
    not an exit of the registry (``login_vault_infra.check_proxy_exit``)."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccount.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    account: str,
    body: LoginVaultAccountUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccount:
    """Change some fields: absent/null = leave, ``""`` = clear, a value = set.

    The secrets are written to the 1Password item, the settings to the row. A
    real change also stamps the row's ``updated_by`` with the caller. 409 while
    the account is archived (restore it first). 422 when a new ``proxy_exit`` is
    not an exit of the registry (``login_vault_infra.check_proxy_exit``)."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccount.model_validate(response.json())
