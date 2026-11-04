"""Set Account Persona Route"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import (
    LoginVaultAccountPersona,
    LoginVaultAccountPersonaUpdate,
)


def _build_request_args(
    login_key: str,
    account: str,
    body: LoginVaultAccountPersonaUpdate,
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
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    login_key: str,
    account: str,
    body: LoginVaultAccountPersonaUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersona:
    """Merge into who the account is, as the login console did: a top-level key omitted stays. `person_key` links the account to that persona (slugified; `""` or null unlinks); a persona that does not exist yet is made with the live email, else the account's username when it is an email, else 422. Inside `live` and `fixture` each key sent replaces that key, an explicit null removes it, the others stay; `"live": null` clears the live identity. `fixture` is the linked persona's, shared by its accounts (422 with no link). A filled live value needs its `source`, a null one a `note`; the fixture's card, bank and id fields take only their placeholders; text that looks like a card number or an SSN is a 422 that never repeats it. 409 for an archived account. A value already held writes nothing. Every vault-org key (person, org-wide, run)."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersona.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    login_key: str,
    account: str,
    body: LoginVaultAccountPersonaUpdate,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultAccountPersona:
    """Merge into who the account is, as the login console did: a top-level key omitted stays. `person_key` links the account to that persona (slugified; `""` or null unlinks); a persona that does not exist yet is made with the live email, else the account's username when it is an email, else 422. Inside `live` and `fixture` each key sent replaces that key, an explicit null removes it, the others stay; `"live": null` clears the live identity. `fixture` is the linked persona's, shared by its accounts (422 with no link). A filled live value needs its `source`, a null one a `note`; the fixture's card, bank and id fields take only their placeholders; text that looks like a card number or an SSN is a 422 that never repeats it. 409 for an archived account. A value already held writes nothing. Every vault-org key (person, org-wide, run)."""

    request_args = _build_request_args(
        login_key=login_key,
        account=account,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultAccountPersona.model_validate(response.json())
