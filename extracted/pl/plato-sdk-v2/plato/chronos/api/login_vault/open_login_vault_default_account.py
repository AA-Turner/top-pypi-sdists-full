"""Open Default Account"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultOpenRequest


def _build_request_args(
    login_key: str,
    body: LoginVaultOpenRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/apps/{login_key}/open"

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
    body: LoginVaultOpenRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> None:
    """Open a browser on the app's default account: the account the clone named `login_key` logs in as by default (`GET /defaults/{clone}`), when it is an account of `login_key` - what `plato vault open <login_key>` picks without `-a`. 404 when the vault has no account of `login_key`; 422 when none of them is the default (open one by name instead); 409 `The default account of <login_key> is archived: ...` naming it when that account is archived (never another account in its place).

    The login world loads the account's newest saved login (`snapshot_ref`;
    null = none the browser can load, so it signs in for real), signs in for real only when an
    agent finds that login signed out, then holds the browser open for `minutes`. The link appears
    on the session page as a preview link labelled `Signed-in browser (<login_key>/<account>)`
    (`GET /api/sessions/{session_id}`, `preview_urls`): noVNC for a VM browser, the Browserbase
    Live View for a `browserbase` account. Nothing is saved unless `save` (VM browsers only).

    A person's own key only; the session is launched as that person and tagged `vault_open`,
    `login_key:<k>`, `account:<a>` and `opened_by:<email>`. 409 (naming the sessions) while the
    live open, bake and run sessions of the account number its `max_sessions` (1 = any one of them)
    or more, or while another launch for it is starting. An open with `save` rewrites the saved
    login, as a bake does, so it is also refused (409) while a bake of the account or another
    saving open is live, whatever `max_sessions` says. 409 `<key>/<acct> was archived on <date> by
    <who>: <reason>; restore it first` for an archived account; 409 also on a 1Password token
    mismatch (as for a bake), and when the login world has no open mode yet."""

    request_args = _build_request_args(
        login_key=login_key,
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
    body: LoginVaultOpenRequest,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> None:
    """Open a browser on the app's default account: the account the clone named `login_key` logs in as by default (`GET /defaults/{clone}`), when it is an account of `login_key` - what `plato vault open <login_key>` picks without `-a`. 404 when the vault has no account of `login_key`; 422 when none of them is the default (open one by name instead); 409 `The default account of <login_key> is archived: ...` naming it when that account is archived (never another account in its place).

    The login world loads the account's newest saved login (`snapshot_ref`;
    null = none the browser can load, so it signs in for real), signs in for real only when an
    agent finds that login signed out, then holds the browser open for `minutes`. The link appears
    on the session page as a preview link labelled `Signed-in browser (<login_key>/<account>)`
    (`GET /api/sessions/{session_id}`, `preview_urls`): noVNC for a VM browser, the Browserbase
    Live View for a `browserbase` account. Nothing is saved unless `save` (VM browsers only).

    A person's own key only; the session is launched as that person and tagged `vault_open`,
    `login_key:<k>`, `account:<a>` and `opened_by:<email>`. 409 (naming the sessions) while the
    live open, bake and run sessions of the account number its `max_sessions` (1 = any one of them)
    or more, or while another launch for it is starting. An open with `save` rewrites the saved
    login, as a bake does, so it is also refused (409) while a bake of the account or another
    saving open is live, whatever `max_sessions` says. 409 `<key>/<acct> was archived on <date> by
    <who>: <reason>; restore it first` for an archived account; 409 also on a 1Password token
    mismatch (as for a bake), and when the login world has no open mode yet."""

    request_args = _build_request_args(
        login_key=login_key,
        body=body,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return None
