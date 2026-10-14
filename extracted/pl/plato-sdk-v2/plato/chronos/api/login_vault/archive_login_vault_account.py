"""Archive Account"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAccountSummary, LoginVaultArchiveRequest


def _build_request_args(
    login_key: str,
    account: str,
    body: LoginVaultArchiveRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/accounts/{login_key}/{account}/archive"

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
    body: LoginVaultArchiveRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountSummary:
    """Archive a dead account (say Google deactivated it), so nothing uses it or takes it over. Sets the account's `archived_at`, `archived_by` (the caller, as `updated_by`) and `archived_reason`, and stamps `updated_by`; 1Password is not touched. The list then hides the account unless `include_archived`; a read still shows it; an open, a bake, an edit and a create of its title get 409 `<key>/<acct> was archived on <date> by <who>: <reason>; restore it first`. Every key of the vault org (person, org-wide, run), for any account. Archiving an archived account changes nothing (200, the first reason is kept). Answers the account without its secrets."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
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
    body: LoginVaultArchiveRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountSummary:
    """Archive a dead account (say Google deactivated it), so nothing uses it or takes it over. Sets the account's `archived_at`, `archived_by` (the caller, as `updated_by`) and `archived_reason`, and stamps `updated_by`; 1Password is not touched. The list then hides the account unless `include_archived`; a read still shows it; an open, a bake, an edit and a create of its title get 409 `<key>/<acct> was archived on <date> by <who>: <reason>; restore it first`. Every key of the vault org (person, org-wide, run), for any account. Archiving an archived account changes nothing (200, the first reason is kept). Answers the account without its secrets."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountSummary.model_validate(response.json())
