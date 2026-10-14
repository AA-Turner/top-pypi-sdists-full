"""Restore Account"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAccountSummary


def _build_request_args(
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/accounts/{login_key}/{account}/restore"

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountSummary:
    """Restore an archived account: clears its `archived_at`, `archived_by` and `archived_reason` and stamps `updated_by`. Every key of the vault org (person, org-wide, run). Restoring an account that is not archived changes nothing (200). Answers the account without its secrets."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountSummary.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    account: str,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountSummary:
    """Restore an archived account: clears its `archived_at`, `archived_by` and `archived_reason` and stamps `updated_by`. Every key of the vault org (person, org-wide, run). Restoring an account that is not archived changes nothing (200). Answers the account without its secrets."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountSummary.model_validate(response.json())
