"""Bake Account"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultBakeRequest


def _build_request_args(
    login_key: str,
    account: str,
    body: LoginVaultBakeRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/accounts/{login_key}/{account}/bake"

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
    login_key: str,
    account: str,
    body: LoginVaultBakeRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> None:
    """Launch a login-world session that signs this account in and saves its snapshot.

    A person's own key only; the session is launched as that person. 409 while
    the account is archived, while the account's last bake, or an open or bake
    session of it, is live, and when that launch would hand the world another
    1Password token than the vault's (``check_bake_token``)."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return None


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    account: str,
    body: LoginVaultBakeRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> None:
    """Launch a login-world session that signs this account in and saves its snapshot.

    A person's own key only; the session is launched as that person. 409 while
    the account is archived, while the account's last bake, or an open or bake
    session of it, is live, and when that launch would hand the world another
    1Password token than the vault's (``check_bake_token``)."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return None
