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
