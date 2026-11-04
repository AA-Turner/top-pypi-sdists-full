"""Update App"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultAppHint, LoginVaultAppHintUpdate


def _build_request_args(
    login_key: str,
    body: LoginVaultAppHintUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/apps/{login_key}"

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
    body: LoginVaultAppHintUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAppHint:
    """Set the app's shared sign-in flow (`login_hint`, trimmed; `""` clears it, null leaves it). Every account of the app reads it, so this is the wide edit; the account's own note is its `login_hint` field. 422 for a hint that runs the sign-in-link opener (`open_login_link.sh`) with no link: the opener fails without one. A value it already holds writes nothing. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        login_key=login_key,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAppHint.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    body: LoginVaultAppHintUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAppHint:
    """Set the app's shared sign-in flow (`login_hint`, trimmed; `""` clears it, null leaves it). Every account of the app reads it, so this is the wide edit; the account's own note is its `login_hint` field. 422 for a hint that runs the sign-in-link opener (`open_login_link.sh`) with no link: the opener fails without one. A value it already holds writes nothing. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        login_key=login_key,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAppHint.model_validate(response.json())
