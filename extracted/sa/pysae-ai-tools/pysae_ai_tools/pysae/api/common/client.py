"""Authenticated HTTP access to the Pysae API.

Resolves the bearer token for an environment (refreshing it silently when the
access token is about to expire) and performs requests against the API base.
Supports three credential modes, in priority order:

1. ``Api-Key`` — ``Authorization: Api-Key <key>`` (the API's ``Api-Key``
   scheme). Best for CI/scripts; no browser, no token store.
2. A raw bearer token supplied out-of-band (``$PYSAE_API_TOKEN``).
3. The stored Auth0 token set, auto-refreshed via the refresh token.
"""

import os
from dataclasses import dataclass

import httpx

from . import oauth, tokens
from .config import Auth0Env, resolve_client_id

_DEFAULT_TIMEOUT = 60.0


class NotAuthenticated(RuntimeError):
    """Raised when no usable credential is available for an environment."""


@dataclass
class Credential:
    """An ``Authorization`` header value plus how it was obtained."""

    header: str
    kind: str  # "api-key" | "env-token" | "oauth"


def _api_key(env: Auth0Env, override: str | None) -> str | None:
    if override:
        return override
    return os.environ.get(f"PYSAE_API_KEY_{env.name.upper()}") or os.environ.get("PYSAE_API_KEY")


def _env_token(env: Auth0Env) -> str | None:
    return os.environ.get(f"PYSAE_API_TOKEN_{env.name.upper()}") or os.environ.get("PYSAE_API_TOKEN")


def resolve_credential(
    env: Auth0Env,
    *,
    api_key: str | None = None,
    client_id: str | None = None,
) -> Credential:
    """Resolve an ``Authorization`` header for ``env``.

    Refreshes and persists the OAuth token when it is expired. Raises
    :class:`NotAuthenticated` when nothing usable is found.
    """
    key = _api_key(env, api_key)
    if key:
        return Credential(header=f"Api-Key {key}", kind="api-key")

    raw = _env_token(env)
    if raw:
        return Credential(header=f"Bearer {raw}", kind="env-token")

    stored = tokens.load(env.name)
    if stored is None:
        raise NotAuthenticated(
            f"not logged in to '{env.name}'. Run: pysae-ai-tools pysae api auth login --env {env.name}"
        )

    if stored.is_expired():
        cid = resolve_client_id(env, client_id)
        try:
            refreshed = oauth.refresh(env, cid, stored)
        except oauth.OAuthError as e:
            raise NotAuthenticated(
                f"session for '{env.name}' expired and refresh failed ({e}). "
                f"Run: pysae-ai-tools pysae api auth login --env {env.name}"
            ) from e
        tokens.save(env.name, refreshed)
        stored = refreshed

    return Credential(header=f"{stored.token_type} {stored.access_token}", kind="oauth")


def request(
    env: Auth0Env,
    method: str,
    path: str,
    *,
    credential: Credential,
    params: list[tuple[str, str]] | None = None,
    json_body: object | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = _DEFAULT_TIMEOUT,
) -> httpx.Response:
    """Perform an authenticated request and return the raw response."""
    url = path if path.startswith("http") else env.api_base + ("" if path.startswith("/") else "/") + path
    final_headers = {"Authorization": credential.header, "Accept": "application/json"}
    if headers:
        final_headers.update(headers)
    query = httpx.QueryParams(tuple(params)) if params else None
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        return client.request(
            method.upper(),
            url,
            params=query,
            json=json_body,
            headers=final_headers,
        )
