"""Set Persona Route"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultPersona, LoginVaultPersonaUpdate


def _build_request_args(
    persona: str,
    body: LoginVaultPersonaUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/personas/{persona}"

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
    persona: str,
    body: LoginVaultPersonaUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultPersona:
    """Create the persona or merge into it. Per field: null leaves it, `""` clears it, a value sets it. `email` (trimmed, lower-cased) is required to create one and cannot be cleared; 409 when it is another persona's. `phone` is normalized as an account's is; 422 when it holds no number, and when it is a NEW number its `sms-` item marks `deprecated` (keeping the number the persona has is fine). The number pool is read first, so a 1Password failure (502/503) writes nothing. `fixture` (the person's data-only identity, shared by its accounts) merges: omitted leaves it, null clears it, each key sent replaces that key and a null key removes it; its card, bank and id fields take only their placeholders, and text that looks like a card number or an SSN is a 422 that never repeats it. A value it already holds writes nothing. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        persona=persona,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultPersona.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    persona: str,
    body: LoginVaultPersonaUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultPersona:
    """Create the persona or merge into it. Per field: null leaves it, `""` clears it, a value sets it. `email` (trimmed, lower-cased) is required to create one and cannot be cleared; 409 when it is another persona's. `phone` is normalized as an account's is; 422 when it holds no number, and when it is a NEW number its `sms-` item marks `deprecated` (keeping the number the persona has is fine). The number pool is read first, so a 1Password failure (502/503) writes nothing. `fixture` (the person's data-only identity, shared by its accounts) merges: omitted leaves it, null clears it, each key sent replaces that key and a null key removes it; its card, bank and id fields take only their placeholders, and text that looks like a card number or an SSN is a 422 that never repeats it. A value it already holds writes nothing. Every key of the vault org (person, org-wide, run)."""

    request_args = _build_request_args(
        persona=persona,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultPersona.model_validate(response.json())
