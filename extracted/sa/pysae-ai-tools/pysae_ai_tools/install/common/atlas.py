"""Shared helpers for the MongoDB Atlas MCP server installers (dev/prod/org).

Atlas API keys are fetched per user from AWS Secrets Manager: the dev/prod
servers read ``mongodb-atlas-public-key`` / ``mongodb-atlas-private-key`` from
``iam/<username>/<env>/atlas``; the org server reads
``mongodb-atlas-org-public-key`` / ``mongodb-atlas-org-private-key`` from the
env-agnostic ``iam/<username>/atlas``.

An explicit ``ATLAS_<ENV>_PUBLIC_KEY`` / ``ATLAS_<ENV>_PRIVATE_KEY`` (or
``ATLAS_ORG_*``) env var pair overrides the secret — the mechanism used to
inject keys in CI without an AWS round-trip.
"""

from os import environ
from typing import Any

from ...env import secret_store
from .base import McpTool


def fetch_project_keys(env: str) -> tuple[str, str]:
    """Fetch the project-scoped ``(public_key, private_key)`` for ``env``.

    Reads ``iam/<username>/<env>/atlas`` (via the shared secret store) and
    extracts the ``mongodb-atlas-public-key`` / ``mongodb-atlas-private-key``
    fields.
    """
    secret_id = secret_store.user_secret_id("atlas", env)
    data = secret_store.fetch_secret(secret_id)
    pub = data.get("mongodb-atlas-public-key", "")
    priv = data.get("mongodb-atlas-private-key", "")
    if not pub or not priv:
        raise RuntimeError(f"{secret_id}: missing mongodb-atlas-public-key / mongodb-atlas-private-key fields")
    return pub, priv


def fetch_org_keys() -> tuple[str, str]:
    """Fetch the organisation-scoped ``(public_key, private_key)``.

    Reads the env-agnostic ``iam/<username>/atlas`` secret (via the shared
    secret store) and extracts the ``mongodb-atlas-org-public-key`` /
    ``mongodb-atlas-org-private-key`` fields.
    """
    secret_id = secret_store.user_secret_id("atlas")
    data = secret_store.fetch_secret(secret_id)
    pub = data.get("mongodb-atlas-org-public-key", "")
    priv = data.get("mongodb-atlas-org-private-key", "")
    if not pub or not priv:
        raise RuntimeError(f"{secret_id}: missing mongodb-atlas-org-public-key / mongodb-atlas-org-private-key fields")
    return pub, priv


def resolve_project_keys(env: str) -> tuple[str, str]:
    """Env-var override (``ATLAS_<ENV>_PUBLIC_KEY``/``…_PRIVATE_KEY``) or secret."""
    prefix = f"ATLAS_{env.upper()}"
    if environ.get(f"{prefix}_PUBLIC_KEY"):
        return environ[f"{prefix}_PUBLIC_KEY"], environ[f"{prefix}_PRIVATE_KEY"]
    return fetch_project_keys(env)


def resolve_org_keys() -> tuple[str, str]:
    """Env-var override (``ATLAS_ORG_PUBLIC_KEY``/``…_PRIVATE_KEY``) or secret."""
    if environ.get("ATLAS_ORG_PUBLIC_KEY"):
        return environ["ATLAS_ORG_PUBLIC_KEY"], environ["ATLAS_ORG_PRIVATE_KEY"]
    return fetch_org_keys()


def build_server(public_key: str, private_key: str) -> dict[str, Any]:
    return {
        "command": "npx",
        "args": ["mcp-mongodb-atlas"],
        "env": {"ATLAS_PUBLIC_KEY": public_key, "ATLAS_PRIVATE_KEY": private_key},
    }


class AtlasMcpTool(McpTool):
    """Base installer for a single MongoDB Atlas MCP server (dev/prod/org).

    Subclasses set :attr:`name` / :attr:`server_name` and implement
    :meth:`resolve_keys`. The stores carry the secret-free shim entry; the keys
    are resolved from AWS Secrets Manager by :meth:`build_config` at launch,
    through the shim.
    """

    server_name: str
    secret_env: str | None = None  # "dev"/"prod" for project servers, None for org

    def resolve_keys(self) -> tuple[str, str]:
        """Return ``(public_key, private_key)`` for this server."""
        raise NotImplementedError

    def build_config(self) -> dict[str, Any]:
        pub, priv = self.resolve_keys()
        return build_server(pub, priv)

    def secret_ids(self) -> tuple[str, ...]:
        """AWS secret id this server reads — lets the installer preload it in parallel."""
        try:
            return (secret_store.user_secret_id("atlas", self.secret_env),)
        except secret_store.SecretError:
            return ()
