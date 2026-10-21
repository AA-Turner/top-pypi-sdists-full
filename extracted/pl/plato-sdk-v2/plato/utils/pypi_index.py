"""Plato-hosted PyPI Simple API URLs (token authentication)."""

from __future__ import annotations

import os
import re

_TOKEN_CREDENTIAL_IN_URL = re.compile(r"(__token__:)([^@]+)(@)")


def redact_pypi_token_credential(text: str) -> str:
    """Replace embedded `__token__:<secret>@` segments (safe for logs)."""
    return _TOKEN_CREDENTIAL_IN_URL.sub(r"\1***\3", text)


def plato_token_simple_index(repo: str, *, api_key: str | None = None) -> str:
    """Return authenticated Simple index URL for a repo (e.g. pypi-store, agents, worlds)."""
    key = api_key if api_key is not None else os.environ.get("PLATO_API_KEY", "")
    return f"https://__token__:{key}@plato.so/api/v2/pypi/{repo}/simple/"


def plato_build_env(*, api_key: str | None = None, base: dict[str, str] | None = None) -> dict[str, str] | None:
    """Subprocess env that lets uv resolve plato-sdk-v2 during builds.

    plato-sdk-v2 is private (Plato pypi-store CodeArtifact repo, which
    upstreams pypi.org for public packages). PEP 517 isolated builds resolve
    [build-system].requires from the configured indexes, and uv sync/lock in
    agent/world checkouts resolve the SDK runtime dep the same way — this adds
    the authenticated pypi-store index to the caller's extra indexes so those succeed.

    Starts from ``base`` (default: os.environ). Returns None (inherit the
    caller's env unchanged) when no API key is available, leaving default
    resolution intact.
    """
    key = api_key if api_key is not None else os.environ.get("PLATO_API_KEY", "")
    if not key:
        return None
    env = dict(os.environ if base is None else base)
    plato_index = plato_token_simple_index("pypi-store", api_key=key)
    extra_indexes = env.get("UV_EXTRA_INDEX_URL", "").split()
    if plato_index not in extra_indexes:
        extra_indexes.append(plato_index)
    env["UV_EXTRA_INDEX_URL"] = " ".join(extra_indexes)
    env["UV_INDEX_STRATEGY"] = "unsafe-best-match"
    # Credentials for pyprojects that declare the index by name
    # ([[tool.uv.index]] name = "plato-store") instead of relying on the
    # extra-index env var.
    env["UV_INDEX_PLATO_STORE_USERNAME"] = "__token__"
    env["UV_INDEX_PLATO_STORE_PASSWORD"] = key
    return env
