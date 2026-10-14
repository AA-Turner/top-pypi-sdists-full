"""Import Settings Route"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultImportResult


def _build_request_args(
    dry_run: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/login-vault/import-settings"

    params: dict[str, Any] = {}
    if dry_run is not None:
        params["dry_run"] = dry_run

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    dry_run: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultImportResult:
    """Copy the old 1Password settings items into Chronos, once: `login-defaults` into the defaults, `login-hints` into the app hints, `proxy-bans` and `proxy-ban-notes` into the exit bans (one ban per exit and app, `*` for every app, with the note's reason, by and at when it has one). A table the import already ran for (also one emptied since), or that already has rows, is refused (`refused` says so) and left as it is; the others are filled. `dry_run`: read and count only, and records nothing. `skipped` names the item fields that hold no row (never a value). The items are only read. A person's own key only."""

    request_args = _build_request_args(
        dry_run=dry_run,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultImportResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    dry_run: bool | None = False,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultImportResult:
    """Copy the old 1Password settings items into Chronos, once: `login-defaults` into the defaults, `login-hints` into the app hints, `proxy-bans` and `proxy-ban-notes` into the exit bans (one ban per exit and app, `*` for every app, with the note's reason, by and at when it has one). A table the import already ran for (also one emptied since), or that already has rows, is refused (`refused` says so) and left as it is; the others are filled. `dry_run`: read and count only, and records nothing. `skipped` names the item fields that hold no row (never a value). The items are only read. A person's own key only."""

    request_args = _build_request_args(
        dry_run=dry_run,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultImportResult.model_validate(response.json())
